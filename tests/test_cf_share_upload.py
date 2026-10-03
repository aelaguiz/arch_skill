import json
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HELPER = Path(__file__).resolve().parents[1] / "skills/cf-share/scripts/cf_share.sh"


class ShareUploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.objects = {}
        self.puts = []
        self.purges = []
        self.fail_purge = False
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_PUT(self):
                key = urllib.parse.unquote(self.path.split("/objects/", 1)[1])
                body = self.rfile.read(int(self.headers["Content-Length"]))
                owner.objects[key] = (body, self.headers["Content-Type"], self.headers.get("Cache-Control", ""))
                owner.puts.append(key)
                self.reply({"success": True})

            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                owner.purges.append(payload)
                self.reply({"success": not owner.fail_purge, "result": {}, "errors": ["purge denied"] if owner.fail_purge else []})

            def do_GET(self):
                if self.path.startswith("/api/"):
                    self.reply({"success": True, "result": {"zoneId": "test-zone"}})
                    return
                key = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path.lstrip("/"))
                body, content_type, cache_control = owner.objects[key]
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Cache-Control", cache_control)
                self.send_header("CF-Cache-Status", "BYPASS")
                self.end_headers()
                self.wfile.write(body)

            def reply(self, value):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(value).encode())

            def log_message(self, *_):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        real_curl = shutil.which("curl")
        self.assertIsNotNone(real_curl)
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        curl = bin_dir / "curl"
        curl.write_text(f"""#!/usr/bin/env python3
import os, sys
args = [os.environ['TEST_SHARE_BASE'] + '/api/' + arg.removeprefix('https://api.cloudflare.com/client/v4/') if arg.startswith('https://api.cloudflare.com/client/v4/') else arg for arg in sys.argv[1:]]
os.execv({real_curl!r}, [{real_curl!r}] + args)
""")
        curl.chmod(0o755)
        python = bin_dir / "share-python"
        python.write_text("""#!/usr/bin/env python3
import os, runpy, sys, urllib.request
original = urllib.request.urlopen
def local_open(request, *args, **kwargs):
    if isinstance(request, urllib.request.Request) and request.full_url.startswith('https://api.cloudflare.com/client/v4/'):
        request.full_url = os.environ['TEST_SHARE_BASE'] + '/api/' + request.full_url.removeprefix('https://api.cloudflare.com/client/v4/')
    return original(request, *args, **kwargs)
urllib.request.urlopen = local_open
sys.argv = sys.argv[1:]
if sys.argv[0] == '-c':
    code = sys.argv[1]
    sys.argv = ['-c'] + sys.argv[2:]
    exec(code)
else:
    runpy.run_path(sys.argv[0], run_name='__main__')
""")
        python.chmod(0o755)
        env_file = self.root / "env"
        env_file.write_text(f"CF_SHARE_API_TOKEN=test-token\nCF_SHARE_ACCOUNT_ID=test-account\nCF_SHARE_BUCKET=test-bucket\nCF_SHARE_BASE_URL={self.base}\nCF_SHARE_PYTHON={python}\n")
        self.env = {**os.environ, "CF_SHARE_ENV": str(env_file), "TEST_SHARE_BASE": self.base, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"]}
        self.bundle = self.root / "bundle"
        (self.bundle / "reports").mkdir(parents=True)
        (self.bundle / "assets").mkdir()
        self.entry = self.bundle / "reports/main.html"
        self.entry.write_text('<html><head><title>Current report</title><link rel="stylesheet" href="../assets/style.css"></head><body><p>Concrete findings from the current report revision.</p></body></html>')
        (self.bundle / "assets/style.css").write_text("body {color: red}")

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def publish(self, *flags):
        return subprocess.run(["bash", str(HELPER), "--entry", "reports/main.html", *flags, str(self.bundle)], env=self.env, text=True, capture_output=True, timeout=30)

    def test_cli_preserves_nested_url_updates_assets_and_purges_exact_objects(self):
        first = self.publish()
        self.assertEqual(first.returncode, 0, first.stderr)
        url = next(line.removeprefix("URL: ") for line in first.stdout.splitlines() if line.startswith("URL: "))
        slug = urllib.parse.urlsplit(url).path.split("/")[1]
        self.assertEqual(self.purges, [])
        self.assertEqual(self.puts[-1], slug + "/reports/main.html")
        for body, content_type, cache_control in self.objects.values():
            self.assertIn("no-store", cache_control)
            self.assertIn("no-transform", cache_control)
        (self.bundle / "assets/style.css").write_text("body {color: blue}")
        second = self.publish("--slug", slug)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("URL: " + url, second.stdout)
        self.assertEqual(self.objects[slug + "/assets/style.css"][0], b"body {color: blue}")
        self.assertEqual(len(self.purges), 1)
        self.assertEqual(set(self.purges[0]["files"]), {self.base + "/" + key for key in self.objects})
        self.assertIn("no-store, matching bytes: all 3 objects", second.stdout)

    def test_cli_does_not_print_success_url_when_purge_fails(self):
        self.fail_purge = True
        result = self.publish("--slug", "stable-report")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("URL: ", result.stdout)
        self.assertIn("cache purge failed", result.stderr)
        self.assertIn("keep the requested URL", result.stderr)

    def test_cli_versions_media_in_secondary_pages_and_uploads_prepared_bytes(self):
        media = self.bundle / "assets/clip.mp4"
        media.write_bytes(b"representative media bytes")
        secondary = self.bundle / "reports/details.html"
        original = '<video src="../assets/clip.mp4"></video>'
        secondary.write_text(original)
        self.entry.write_text(self.entry.read_text().replace("</body>", '<iframe src="details.html"></iframe></body>'))
        result = self.publish()
        self.assertEqual(result.returncode, 0, result.stderr)
        key = next(key for key in self.objects if key.endswith("/reports/details.html"))
        served = self.objects[key][0].decode()
        self.assertIn("../assets/clip.mp4?cf_share_v=", served)
        self.assertEqual(secondary.read_text(), original)
        self.assertIn("no-store, matching bytes: all 5 objects", result.stdout)
        self.assertIn("2 media URLs", result.stdout)


if __name__ == "__main__":
    unittest.main()
