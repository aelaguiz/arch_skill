#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


def _http_get(url: str, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
    req = Request(url, headers=headers or {})
    try:
        with urlopen(req, timeout=30) as resp:
            status = getattr(resp, "status", 200)
            raw_headers = {k.lower(): v for k, v in resp.headers.items()}
            return status, raw_headers, resp.read()
    except HTTPError as e:
        raw_headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        body = e.read() if hasattr(e, "read") else b""
        return e.code, raw_headers, body


def _try_parse_openapi_json(body: bytes) -> dict | None:
    text = body.decode("utf-8", errors="replace").strip()
    if not text.startswith("{"):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    if "openapi" in data or "swagger" in data or "paths" in data:
        return data
    return None


def _origin(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def _extract_candidate_urls(html: str, page_url: str) -> list[str]:
    candidates: list[str] = []

    patterns: list[re.Pattern[str]] = [
        re.compile(r"\burl\s*:\s*['\"]([^'\"]+)['\"]"),
        re.compile(r"\"url\"\s*:\s*\"([^\"]+)\""),
        re.compile(r"\bspecUrl\s*:\s*['\"]([^'\"]+)['\"]"),
        re.compile(r"\burls\s*:\s*\[([^\]]+)\]"),
    ]

    for pat in patterns[:3]:
        for m in pat.finditer(html):
            candidates.append(m.group(1).strip())

    # If there's a SwaggerUI "urls" array, capture any inner url entries.
    for m in patterns[3].finditer(html):
        urls_blob = m.group(1)
        for inner in re.finditer(r"\burl\s*:\s*['\"]([^'\"]+)['\"]", urls_blob):
            candidates.append(inner.group(1).strip())

    # Also grab obvious openapi/swagger-ish URLs.
    for m in re.finditer(r"https?://[^'\"\s>]+", html):
        u = m.group(0)
        if any(tok in u.lower() for tok in ("openapi", "swagger", "schema", "api-doc")):
            candidates.append(u)

    # Normalize: resolve relative URLs.
    normalized: list[str] = []
    for u in candidates:
        if not u:
            continue
        # Some swagger configs use relative paths.
        resolved = urljoin(page_url, u)
        normalized.append(resolved)

    # Dedupe while preserving order.
    seen: set[str] = set()
    out: list[str] = []
    for u in normalized:
        if u in seen:
            continue
        seen.add(u)
        out.append(u)

    return out


def _default_out_path() -> Path:
    # Default relative to skill root if run from within the skill.
    here = Path(__file__).resolve()
    skill_root = here.parent.parent
    return skill_root / "references" / "codemagic-openapi.json"


def _iter_fallback_urls(schema_ui_url: str) -> Iterable[str]:
    base_origin = _origin(schema_ui_url)

    # Candidate paths seen in common Swagger/OpenAPI deployments.
    paths = [
        "/api/v3/openapi.json",
        "/api/v3/openapi.yaml",
        "/api/v3/swagger.json",
        "/api/v3/api-docs",
        "/api/v3/schema",
        "/api/v3/schema/openapi.json",
        "/api/v3/schema/swagger.json",
    ]

    for p in paths:
        yield urljoin(base_origin, p)

    # Codemagic may serve API from a different host than the Swagger UI.
    for other_origin in ("https://api.codemagic.io", "https://codemagic.io"):
        for p in paths:
            yield urljoin(other_origin, p)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download Codemagic API v3 OpenAPI schema as JSON (best-effort)."
    )
    parser.add_argument(
        "--schema-ui-url",
        default=(
            ("https://codemagic.io/api/v3/schema")
        ),
        help="Swagger UI page URL (hash fragment is ignored).",
    )
    parser.add_argument(
        "--out",
        default=str(_default_out_path()),
        help="Output path for the OpenAPI JSON.",
    )
    parser.add_argument(
        "--print-url",
        action="store_true",
        help="Print the resolved spec URL to stdout.",
    )

    args = parser.parse_args()

    schema_ui_url = args.schema_ui_url.split("#", 1)[0]

    headers = {
        "User-Agent": "codemagic-builds-skill/1.0",
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    }

    html = ""
    status, resp_headers, body = _http_get(schema_ui_url, headers=headers)
    if status >= 200 and status < 300 and body:
        ct = resp_headers.get("content-type", "")
        # Sometimes the UI URL *is* the schema.
        maybe_schema = _try_parse_openapi_json(body)
        if maybe_schema is not None:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(maybe_schema, indent=2, sort_keys=True) + "\n")
            if args.print_url:
                print(schema_ui_url)
            return 0

        if "html" in ct or body.lstrip().startswith(b"<!doctype") or body.lstrip().startswith(b"<"):
            html = body.decode("utf-8", errors="replace")

    candidates: list[str] = []
    if html:
        candidates.extend(_extract_candidate_urls(html, schema_ui_url))

    candidates.extend(list(_iter_fallback_urls(schema_ui_url)))

    # Dedupe.
    seen: set[str] = set()
    final_candidates: list[str] = []
    for u in candidates:
        if u in seen:
            continue
        seen.add(u)
        final_candidates.append(u)

    last_error: str | None = None

    for u in final_candidates:
        try:
            s, h, b = _http_get(u, headers={"User-Agent": headers["User-Agent"], "Accept": "application/json"})
            if s < 200 or s >= 300 or not b:
                last_error = f"HTTP {s} from {u}"
                continue

            schema = _try_parse_openapi_json(b)
            if schema is None:
                last_error = f"Non-OpenAPI JSON from {u}"
                continue

            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")

            if args.print_url:
                print(u)

            return 0
        except URLError as e:
            last_error = f"URL error from {u}: {e}"

    sys.stderr.write("Failed to locate Codemagic OpenAPI schema URL.\n")
    if last_error:
        sys.stderr.write(f"Last error: {last_error}\n")
    sys.stderr.write("Tip: open the Swagger UI in a browser and look for the configured spec URL, then pass it via --schema-ui-url or adjust fallbacks.\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
