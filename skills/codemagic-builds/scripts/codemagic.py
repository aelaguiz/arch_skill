#!/usr/bin/env python3

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _json_dumps(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def _read_json_path(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _coalesce(*vals: Any) -> Any:
    for v in vals:
        if v is not None and v != "":
            return v
    return None


def _dig(obj: Any, *keys: str) -> Any:
    cur = obj
    for k in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return None if cur == "" else cur


def _first_matching_value(obj: dict[str, Any], keys: list[str]) -> Any:
    for k in keys:
        if k in obj and obj[k] not in (None, ""):
            return obj[k]
    return None


def _stringify(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    return str(v)


def _short(s: str, max_len: int = 120) -> str:
    s = (s or "").replace("\n", " ").strip()
    return s if len(s) <= max_len else (s[: max_len - 1] + "…")


def _parse_iso_datetime(s: str) -> datetime | None:
    s = (s or "").strip()
    if not s:
        return None

    # Handle common Z suffix.
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


def _parse_since(since: str) -> datetime | None:
    # Supports ISO timestamps. Keep intentionally minimal.
    return _parse_iso_datetime(since)


@dataclass
class CodemagicClient:
    base_url: str
    token: str
    auth_mode: str

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "User-Agent": "codemagic-builds-skill/1.0",
            "Accept": "application/json",
        }

        if self.token and self.auth_mode != "none":
            mode = self.auth_mode.lower().strip()
            if mode in ("x-auth-token", "x_auth_token", "xauth", "token"):
                headers["x-auth-token"] = self.token
            elif mode in ("bearer", "authorization"):
                headers["Authorization"] = f"Bearer {self.token}"
            else:
                raise ValueError(f"Unsupported CM_API_AUTH mode: {self.auth_mode}")

        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, str] | None = None,
        json_body: Any | None = None,
        absolute_url: str | None = None,
    ) -> tuple[int, Any, dict[str, str]]:
        url = absolute_url or (self.base_url.rstrip("/") + "/" + path.lstrip("/"))
        if query:
            url += ("?" + urlencode(query, doseq=True))

        body_bytes: bytes | None = None
        headers = self._headers()

        if json_body is not None:
            body_bytes = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = Request(url, method=method.upper(), headers=headers, data=body_bytes)
        try:
            with urlopen(req, timeout=60) as resp:
                raw = resp.read()
                status = getattr(resp, "status", 200)
                resp_headers = {k.lower(): v for k, v in resp.headers.items()}
                return status, _parse_json_or_text(raw, resp_headers.get("content-type", "")), resp_headers
        except HTTPError as e:
            raw = e.read()
            resp_headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
            return e.code, _parse_json_or_text(raw, resp_headers.get("content-type", "")), resp_headers


def _parse_json_or_text(raw: bytes, content_type: str) -> Any:
    if not raw:
        return None
    text = raw.decode("utf-8", errors="replace")
    if "json" in (content_type or "").lower() or text.lstrip().startswith("{") or text.lstrip().startswith("["):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    return text


def _normalize_list(payload: Any, list_keys: Iterable[str]) -> list[dict[str, Any]]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [b for b in payload if isinstance(b, dict)]
    if isinstance(payload, dict):
        for key in list_keys:
            v = payload.get(key)
            if isinstance(v, list):
                return [b for b in v if isinstance(b, dict)]
    return []


def _normalize_build_list(payload: Any) -> list[dict[str, Any]]:
    return _normalize_list(payload, ["builds", "data", "items", "results"])


def _normalize_apps_list(payload: Any) -> list[dict[str, Any]]:
    return _normalize_list(payload, ["apps", "applications", "data", "items", "results"])


def _normalize_vars_list(payload: Any) -> list[dict[str, Any]]:
    return _normalize_list(payload, ["variables", "environmentVariables", "envVars", "data", "items", "results"])


def _build_status(build: dict[str, Any]) -> str:
    return _stringify(_first_matching_value(build, ["status", "buildStatus", "state"]) or "unknown")


def _build_id(build: dict[str, Any]) -> str:
    return _stringify(_first_matching_value(build, ["id", "buildId", "build_id"]) or "")


def _build_file_workflow_id(build: dict[str, Any]) -> str:
    return _stringify(_coalesce(build.get("fileWorkflowId"), build.get("file_workflow_id"), _dig(build, "workflow", "fileWorkflowId")) or "")


def _build_app_id(build: dict[str, Any]) -> str:
    return _stringify(
        _coalesce(
            _dig(build, "app", "id"),
            _dig(build, "application", "id"),
            build.get("appId"),
            build.get("applicationId"),
        )
        or ""
    )


def _build_workflow_id(build: dict[str, Any]) -> str:
    return _stringify(_coalesce(build.get("workflowId"), build.get("workflow_id"), _dig(build, "workflow", "id")) or "")


def _build_workflow_name(build: dict[str, Any]) -> str:
    return _stringify(_coalesce(build.get("workflowName"), build.get("workflow_name"), _dig(build, "workflow", "name")) or "")


def _build_branch(build: dict[str, Any]) -> str:
    return _stringify(_coalesce(build.get("branch"), _dig(build, "commit", "branch"), _dig(build, "scm", "branch")) or "")


def _build_message(build: dict[str, Any]) -> str:
    return _short(
        _stringify(
            _coalesce(
                build.get("message"),
                build.get("commitMessage"),
                _dig(build, "commit", "message"),
                build.get("triggeredBy"),
            )
            or ""
        )
    )


def _build_platform(build: dict[str, Any]) -> str:
    plat = _coalesce(
        build.get("platform"),
        build.get("appType"),
        build.get("applicationType"),
        _dig(build, "app", "platform"),
        _dig(build, "application", "platform"),
        _dig(build, "workflow", "platform"),
    )
    if not plat:
        return ""
    s = _stringify(plat).lower()
    if "android" in s:
        return "android"
    if "ios" in s:
        return "ios"
    return _stringify(plat)


def _build_created_at(build: dict[str, Any]) -> str:
    return _stringify(_coalesce(build.get("createdAt"), build.get("created_at"), build.get("startedAt"), build.get("startTime")) or "")


def _build_timestamps(build: dict[str, Any]) -> tuple[str, str]:
    started = _stringify(_coalesce(build.get("startedAt"), build.get("startTime"), build.get("createdAt")) or "")
    finished = _stringify(_coalesce(build.get("finishedAt"), build.get("finishTime"), build.get("updatedAt")) or "")
    return started, finished


def _extract_failure_summary(build: dict[str, Any]) -> str:
    msg = _coalesce(
        build.get("message"),
        build.get("error"),
        build.get("errorMessage"),
        build.get("failureReason"),
        build.get("reason"),
        _dig(build, "build", "error"),
        _dig(build, "failure", "message"),
    )

    steps = _coalesce(build.get("steps"), build.get("buildSteps"), _dig(build, "build", "steps"))
    if isinstance(steps, list):
        for step in steps:
            if not isinstance(step, dict):
                continue
            st = _stringify(_coalesce(step.get("status"), step.get("state")) or "").lower()
            if st in ("failed", "error"):
                step_name = _stringify(_coalesce(step.get("name"), step.get("title")) or "")
                step_msg = _coalesce(step.get("message"), step.get("error"), step.get("errorMessage"))
                if step_name and step_msg:
                    return _short(f"{step_name}: {_stringify(step_msg)}")
                if step_msg:
                    return _short(_stringify(step_msg))
                if step_name:
                    return _short(step_name)

    if msg:
        return _short(_stringify(msg))

    return ""


def _print_build_line(build: dict[str, Any], *, env: str | None = None) -> None:
    bid = _build_id(build)
    status = _build_status(build)
    plat = _build_platform(build)
    branch = _build_branch(build)
    wf = _build_workflow_name(build) or _build_workflow_id(build)
    started, finished = _build_timestamps(build)

    parts = []
    if env:
        parts.append(env)
    if plat:
        parts.append(plat)
    parts.append(status)
    if wf:
        parts.append(wf)
    if branch:
        parts.append(branch)
    if started:
        parts.append(started)
    if finished and finished != started:
        parts.append(finished)

    line = " | ".join(parts)
    if bid:
        line = f"{bid} | " + line
    print(line)


def _print_build_minimal_line(build: dict[str, Any]) -> None:
    parts = [
        _build_id(build),
        _build_status(build),
        _build_file_workflow_id(build),
        _build_workflow_name(build) or _build_workflow_id(build),
        _build_branch(build),
        _build_message(build),
        _build_created_at(build),
    ]
    print(" | ".join([p if p is not None else "" for p in parts]))


def _make_client(args: argparse.Namespace) -> CodemagicClient:
    token = args.token or os.getenv("CODEMAGIC_API_TOKEN") or os.getenv("CODEMAGIC_TOKEN") or ""
    if not token and not args.allow_unauthenticated:
        raise SystemExit("Missing CODEMAGIC_API_TOKEN (or pass --token / --allow-unauthenticated).")

    base_url = args.base_url or os.getenv("CM_API_BASE_URL") or "https://api.codemagic.io"
    auth_mode = args.auth or os.getenv("CM_API_AUTH") or "x-auth-token"

    return CodemagicClient(base_url=base_url, token=token, auth_mode=auth_mode)


def _sort_builds_newest_first(builds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(b: dict[str, Any]) -> float:
        dt = _parse_iso_datetime(_build_created_at(b))
        if not dt:
            dt = _parse_iso_datetime(_coalesce(b.get("startedAt"), b.get("createdAt"), "") or "")
        if not dt:
            return 0.0
        return dt.timestamp()

    return sorted(builds, key=key, reverse=True)


def cmd_request(args: argparse.Namespace) -> int:
    client = _make_client(args)

    query: dict[str, str] = {}
    for kv in args.query or []:
        if "=" not in kv:
            raise SystemExit(f"Invalid --query value (expected k=v): {kv}")
        k, v = kv.split("=", 1)
        query[k] = v

    body = _read_json_path(args.body_json) if args.body_json else None

    status, payload, _headers = client.request(args.method, args.path, query=query or None, json_body=body)

    if args.output == "json":
        print(_json_dumps({"status": status, "data": payload}))
        return 0 if 200 <= status < 300 else 2

    if args.quiet:
        # Print raw JSON (or raw text) only.
        if isinstance(payload, (dict, list)):
            print(_json_dumps(payload), end="")
        elif payload is None:
            return 0 if 200 <= status < 300 else 2
        else:
            print(payload)
        return 0 if 200 <= status < 300 else 2

    print(f"HTTP {status}")
    if isinstance(payload, (dict, list)):
        print(_json_dumps(payload))
    else:
        print(payload)

    return 0 if 200 <= status < 300 else 2


def cmd_builds_list(args: argparse.Namespace) -> int:
    client = _make_client(args)

    query: dict[str, str] = {}
    if args.app_id:
        query["appId"] = args.app_id
    if args.workflow_id:
        query["workflowId"] = args.workflow_id
    if args.file_workflow_id:
        query["fileWorkflowId"] = args.file_workflow_id
    if args.branch:
        query["branch"] = args.branch
    if args.status:
        query["status"] = args.status
    query["limit"] = str(args.limit)

    status, payload, _ = client.request("GET", "/builds", query=query)
    builds = _normalize_build_list(payload)

    if args.file_workflow_id:
        builds = [b for b in builds if _build_file_workflow_id(b) == args.file_workflow_id]

    since_dt = _parse_since(args.since) if args.since else None
    if since_dt:
        filtered: list[dict[str, Any]] = []
        for b in builds:
            created_dt = _parse_iso_datetime(_build_created_at(b))
            if created_dt and created_dt >= since_dt:
                filtered.append(b)
        builds = filtered

    builds = _sort_builds_newest_first(builds)

    if args.output == "json":
        print(_json_dumps({"status": status, "builds": builds}))
        return 0 if 200 <= status < 300 else 2

    # Keep legacy text output exactly as before.
    if args.output == "text":
        for b in builds:
            _print_build_line(b)
        return 0 if 200 <= status < 300 else 2

    # Minimal output mode.
    for b in builds:
        _print_build_minimal_line(b)

    return 0 if 200 <= status < 300 else 2


def cmd_builds_in_progress(args: argparse.Namespace) -> int:
    status_filter = args.status or "in_progress"
    candidates = [status_filter]
    if status_filter == "in_progress":
        candidates = ["in_progress", "running", "building", "queued"]

    client = _make_client(args)

    all_builds: list[dict[str, Any]] = []
    for st in candidates:
        query = {"limit": str(args.limit), "status": st}
        if args.app_id:
            query["appId"] = args.app_id
        if args.workflow_id:
            query["workflowId"] = args.workflow_id
        s, payload, _ = client.request("GET", "/builds", query=query)
        if not (200 <= s < 300):
            continue
        all_builds.extend(_normalize_build_list(payload))

    seen: set[str] = set()
    builds: list[dict[str, Any]] = []
    for b in all_builds:
        bid = _build_id(b)
        if not bid or bid in seen:
            continue
        seen.add(bid)
        builds.append(b)

    builds = _sort_builds_newest_first(builds)

    if args.output == "json":
        print(_json_dumps({"generatedAt": _utc_now_iso(), "builds": builds}))
        return 0

    if not builds:
        print("No in-progress builds found (or API does not support status filtering).")
        return 0

    for b in builds:
        _print_build_line(b)

    return 0


def cmd_builds_get(args: argparse.Namespace) -> int:
    client = _make_client(args)

    status, payload, _ = client.request("GET", f"/builds/{args.build_id}")

    print(_json_dumps({"status": status, "build": payload}))

    if not (args.steps or args.step_logs):
        return 0 if 200 <= status < 300 else 2

    build = payload if isinstance(payload, dict) else {}
    steps = _extract_build_steps(build)

    if args.steps:
        if not steps:
            print("(No build actions/steps found)")
        else:
            for idx, step in enumerate(steps, start=1):
                name = step.get("name") or "(unnamed)"
                st = step.get("status") or ""
                url = step.get("logUrl") or ""
                print(f"{idx}. {name} | {st} | {url}")

    if args.step_logs:
        tail_lines = args.tail
        selected = _select_steps_for_logs(steps, step_index=args.step_index, name_contains=args.step_name_contains)
        if not selected:
            print("(No step logs available)")
        for idx, step in selected:
            url = step.get("logUrl")
            if not url:
                continue
            log_text = _fetch_text_url(client, url)
            print(f"--- step {idx}: {step.get('name') or '(unnamed)'}")
            print(_tail_text_lines(log_text, tail_lines))

    return 0 if 200 <= status < 300 else 2


def _extract_build_steps(build: dict[str, Any]) -> list[dict[str, Any]]:
    # v3 often uses buildActions; older APIs may use actions/steps.
    actions = _coalesce(build.get("buildActions"), build.get("actions"), build.get("steps"), _dig(build, "build", "actions"))
    if not isinstance(actions, list):
        return []

    steps: list[dict[str, Any]] = []
    for a in actions:
        if not isinstance(a, dict):
            continue
        name = _stringify(_coalesce(a.get("name"), a.get("title"), a.get("action")) or "")
        status = _stringify(_coalesce(a.get("status"), a.get("state"), a.get("result")) or "")
        log_url = _stringify(_coalesce(a.get("logUrl"), a.get("log_url"), a.get("logURL"), a.get("url")) or "")
        steps.append({"name": name, "status": status, "logUrl": log_url})

    return steps


def _fetch_text_url(client: CodemagicClient, url: str) -> str:
    s, payload, headers = client.request("GET", "/", absolute_url=url)
    if isinstance(payload, (dict, list)):
        return _json_dumps(payload)
    return "" if payload is None else str(payload)


def _tail_text_lines(text: str, n: int) -> str:
    lines = (text or "").splitlines()
    tail = lines[-n:] if n > 0 else lines
    return "\n".join(tail) + ("\n" if tail else "")


def _select_steps_for_logs(
    steps: list[dict[str, Any]],
    *,
    step_index: int | None,
    name_contains: str | None,
) -> list[tuple[int, dict[str, Any]]]:
    if not steps:
        return []

    if step_index is not None:
        if 1 <= step_index <= len(steps):
            return [(step_index, steps[step_index - 1])]
        return []

    if name_contains:
        needle = name_contains.lower()
        matches: list[tuple[int, dict[str, Any]]] = []
        for i, s in enumerate(steps, start=1):
            if needle in (s.get("name") or "").lower():
                matches.append((i, s))
        if matches:
            return matches

    # Default: prefer failed steps, otherwise the last step.
    failed: list[tuple[int, dict[str, Any]]] = []
    for i, s in enumerate(steps, start=1):
        st = (s.get("status") or "").lower()
        if st in ("failed", "error"):
            failed.append((i, s))

    if failed:
        return failed

    return [(len(steps), steps[-1])]


def cmd_builds_cancel(args: argparse.Namespace) -> int:
    client = _make_client(args)

    status, payload, _ = client.request("POST", f"/builds/{args.build_id}/cancel")

    print(_json_dumps({"status": status, "data": payload}))
    return 0 if 200 <= status < 300 else 2


def cmd_builds_cancel_running(args: argparse.Namespace) -> int:
    if not args.yes:
        raise SystemExit("Refusing to cancel builds without --yes.")

    client = _make_client(args)

    query: dict[str, str] = {"limit": str(args.limit)}
    if args.app_id:
        query["appId"] = args.app_id
    if args.workflow_id:
        query["workflowId"] = args.workflow_id

    cancelled: list[dict[str, Any]] = []

    for st in ("in_progress", "running", "building", "queued"):
        query_with_status = dict(query)
        query_with_status["status"] = st
        s, payload, _ = client.request("GET", "/builds", query=query_with_status)
        if not (200 <= s < 300):
            continue
        builds = _normalize_build_list(payload)
        for b in builds:
            bid = _build_id(b)
            if not bid:
                continue
            cs, cpayload, _ = client.request("POST", f"/builds/{bid}/cancel")
            cancelled.append({"buildId": bid, "cancelStatus": cs, "response": cpayload})

    print(_json_dumps({"cancelled": cancelled}))
    return 0


def cmd_builds_start(args: argparse.Namespace) -> int:
    client = _make_client(args)

    body: dict[str, Any] = {
        "appId": args.app_id,
        "workflowId": args.workflow_id,
    }
    if args.branch:
        body["branch"] = args.branch
    if args.tag:
        body["tag"] = args.tag

    if args.extra_json:
        extra = _read_json_path(args.extra_json)
        if isinstance(extra, dict):
            body.update(extra)

    status, payload, _ = client.request("POST", "/builds", json_body=body)

    print(_json_dumps({"status": status, "data": payload}))
    return 0 if 200 <= status < 300 else 2


def _status_is_failure(status: str) -> bool:
    s = (status or "").strip().lower()
    return s in ("failed", "error")


def cmd_builds_failures(args: argparse.Namespace) -> int:
    client = _make_client(args)

    base_query: dict[str, str] = {"limit": str(args.limit)}
    if args.app_id:
        base_query["appId"] = args.app_id
    if args.workflow_id:
        base_query["workflowId"] = args.workflow_id

    statuses = [args.status] if args.status else ["failed", "error"]
    status_values = [s.strip().lower() for s in statuses if s]

    builds: list[dict[str, Any]] = []
    status_filtered_supported = False

    for st in statuses:
        query_with_status = dict(base_query)
        query_with_status["status"] = st
        s, payload, _ = client.request("GET", "/builds", query=query_with_status)
        if 200 <= s < 300:
            status_filtered_supported = True
            builds.extend(_normalize_build_list(payload))

    deduped = _dedupe_builds(builds)
    if status_values:
        deduped = [b for b in deduped if _build_status(b).strip().lower() in status_values]

    # Client-side fallback when status filtering is unsupported or returns nothing.
    if (not status_filtered_supported) or (not deduped):
        s, payload, _ = client.request("GET", "/builds", query=base_query)
        if 200 <= s < 300:
            all_builds = _normalize_build_list(payload)
            if status_values:
                filtered = [b for b in all_builds if _build_status(b).strip().lower() in status_values]
            else:
                filtered = [b for b in all_builds if _status_is_failure(_build_status(b))]
            if filtered:
                deduped = _dedupe_builds(filtered)

    if args.output == "json":
        out = []
        for b in deduped:
            out.append(
                {
                    "buildId": _build_id(b),
                    "status": _build_status(b),
                    "platform": _build_platform(b),
                    "appId": _build_app_id(b),
                    "workflowId": _build_workflow_id(b),
                    "workflow": _build_workflow_name(b),
                    "branch": _build_branch(b),
                    "failureSummary": _extract_failure_summary(b),
                }
            )
        print(_json_dumps({"generatedAt": _utc_now_iso(), "failures": out}))
        return 0

    if not deduped:
        print("No failed builds found (or API does not support status filtering).")
        return 0

    for b in _sort_builds_newest_first(deduped):
        bid = _build_id(b)
        plat = _build_platform(b)
        wf = _build_workflow_name(b) or _build_workflow_id(b)
        branch = _build_branch(b)
        summary = _extract_failure_summary(b)
        print(" | ".join([p for p in [bid, plat, wf, branch, summary] if p]))

    return 0


def _dedupe_builds(builds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for b in builds:
        bid = _build_id(b)
        if not bid or bid in seen:
            continue
        seen.add(bid)
        deduped.append(b)
    return deduped


def cmd_dashboard(args: argparse.Namespace) -> int:
    client = _make_client(args)
    matrix = _read_json_path(args.matrix)

    envs = matrix.get("environments") if isinstance(matrix, dict) else None
    if not isinstance(envs, dict):
        raise SystemExit("Invalid matrix JSON. Expected top-level { environments: { ... } }.")

    rows: list[tuple[str, str, dict[str, Any] | None]] = []

    for env_name, platforms in envs.items():
        if not isinstance(platforms, dict):
            continue
        for platform, cfg in platforms.items():
            if not isinstance(cfg, dict):
                continue
            app_id = cfg.get("appId")
            workflow_id = cfg.get("workflowId")
            if not app_id or not workflow_id:
                rows.append((env_name, platform, None))
                continue

            query = {
                "limit": "1",
                "appId": str(app_id),
                "workflowId": str(workflow_id),
            }
            s, payload, _ = client.request("GET", "/builds", query=query)
            if not (200 <= s < 300):
                rows.append((env_name, platform, None))
                continue
            builds = _normalize_build_list(payload)
            rows.append((env_name, platform, builds[0] if builds else {}))

    if args.output == "json":
        out = []
        for env_name, platform, build in rows:
            out.append(
                {
                    "environment": env_name,
                    "platform": platform,
                    "build": build,
                }
            )
        print(_json_dumps({"generatedAt": _utc_now_iso(), "rows": out}))
        return 0

    for env_name, platform, build in rows:
        if not build:
            print(f"{env_name} | {platform} | (missing appId/workflowId)")
            continue
        if build == {}:
            print(f"{env_name} | {platform} | (no builds)")
            continue
        _print_build_line(build, env=f"{env_name}/{platform}")

    return 0


def _try_paths(
    client: CodemagicClient,
    *,
    method: str,
    paths: list[str],
    query: dict[str, str] | None = None,
    json_body: Any | None = None,
) -> tuple[int, Any, str]:
    last_status = 0
    last_payload: Any = None

    for p in paths:
        s, payload, _ = client.request(method, p, query=query, json_body=json_body)
        if 200 <= s < 300:
            return s, payload, p
        last_status, last_payload = s, payload

    return last_status, last_payload, paths[-1] if paths else ""


def cmd_apps_list(args: argparse.Namespace) -> int:
    client = _make_client(args)

    paths = ["/apps", "/applications"]
    s, payload, used = _try_paths(client, method="GET", paths=paths)

    apps = _normalize_apps_list(payload)

    if args.output == "json":
        print(_json_dumps({"httpStatus": s, "path": used, "apps": apps}))
        return 0

    for a in apps:
        aid = _stringify(_coalesce(a.get("id"), a.get("appId")) or "")
        name = _stringify(_coalesce(a.get("name"), a.get("appName"), a.get("displayName")) or "")
        if aid or name:
            print(" | ".join([p for p in [aid, name] if p]))

    return 0 if 200 <= s < 300 else 2


def cmd_apps_vars_list(args: argparse.Namespace) -> int:
    client = _make_client(args)

    paths = [
        f"/apps/{args.app_id}/variables",
        f"/apps/{args.app_id}/environment-variables",
        f"/apps/{args.app_id}/environmentVariables",
    ]

    s, payload, used = _try_paths(client, method="GET", paths=paths)

    vars_ = _normalize_vars_list(payload)

    if args.output == "json":
        print(_json_dumps({"httpStatus": s, "path": used, "variables": vars_}))
        return 0

    for v in vars_:
        vid = _stringify(_coalesce(v.get("id"), v.get("varId")) or "")
        group = _stringify(_coalesce(v.get("group"), v.get("groupName")) or "")
        key = _stringify(_coalesce(v.get("key"), v.get("name")) or "")
        secure = _stringify(_coalesce(v.get("secure"), v.get("isSecure"), v.get("sensitive"), v.get("isSensitive")) or "")
        print(" | ".join([p for p in [vid, group, key, secure] if p]))

    return 0 if 200 <= s < 300 else 2


def cmd_apps_vars_add(args: argparse.Namespace) -> int:
    client = _make_client(args)

    body: dict[str, Any] = {
        "group": args.group,
        "key": args.key,
        "value": args.value,
        "secure": bool(args.secure),
    }

    paths = [
        f"/apps/{args.app_id}/variables",
        f"/apps/{args.app_id}/environment-variables",
        f"/apps/{args.app_id}/environmentVariables",
    ]

    s, payload, used = _try_paths(client, method="POST", paths=paths, json_body=body)

    print(_json_dumps({"httpStatus": s, "path": used, "data": payload}))
    return 0 if 200 <= s < 300 else 2


def cmd_apps_vars_delete(args: argparse.Namespace) -> int:
    client = _make_client(args)

    paths = [
        f"/apps/{args.app_id}/variables/{args.var_id}",
        f"/apps/{args.app_id}/environment-variables/{args.var_id}",
        f"/apps/{args.app_id}/environmentVariables/{args.var_id}",
    ]

    s, payload, used = _try_paths(client, method="DELETE", paths=paths)

    print(_json_dumps({"httpStatus": s, "path": used, "data": payload}))
    return 0 if 200 <= s < 300 else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Codemagic helper CLI for querying builds and managing build runs."
    )

    p.add_argument("--base-url", help="Override CM_API_BASE_URL")
    p.add_argument("--token", help="Override CODEMAGIC_API_TOKEN")
    p.add_argument("--auth", help="Override CM_API_AUTH (x-auth-token|bearer|none)")
    p.add_argument(
        "--allow-unauthenticated",
        action="store_true",
        help="Allow requests without CODEMAGIC_API_TOKEN (for public endpoints).",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    req = sub.add_parser("request", help="Make a raw request (debugging/probing).")
    req.add_argument("method")
    req.add_argument("path")
    req.add_argument("--query", action="append", help="Query param k=v (repeatable)")
    req.add_argument("--json", dest="body_json", help="Path to JSON body file")
    req.add_argument("--body-json", dest="body_json", help="Path to JSON body file")
    req.add_argument("--output", choices=["json", "text"], default="text")
    req.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the HTTP status line and print raw JSON/text only.",
    )
    req.set_defaults(func=cmd_request)

    builds = sub.add_parser("builds", help="Build-related operations")
    builds_sub = builds.add_subparsers(dest="builds_cmd", required=True)

    b_list = builds_sub.add_parser("list", help="List builds (legacy text output by default)")
    b_list.add_argument("--app-id")
    b_list.add_argument("--workflow-id")
    b_list.add_argument("--file-workflow-id")
    b_list.add_argument("--branch")
    b_list.add_argument("--status")
    b_list.add_argument("--since", help="ISO timestamp (e.g. 2026-02-04T00:00:00Z)")
    b_list.add_argument("--limit", type=int, default=20)
    b_list.add_argument("--output", choices=["json", "text", "minimal"], default="text")
    b_list.set_defaults(func=cmd_builds_list)

    b_ip = builds_sub.add_parser("in-progress", help="Summarize builds in progress")
    b_ip.add_argument("--app-id")
    b_ip.add_argument("--workflow-id")
    b_ip.add_argument("--status", help="Override in-progress status string")
    b_ip.add_argument("--limit", type=int, default=20)
    b_ip.add_argument("--output", choices=["json", "text"], default="text")
    b_ip.set_defaults(func=cmd_builds_in_progress)

    b_get = builds_sub.add_parser("get", help="Get build details")
    b_get.add_argument("--build-id", required=True)
    b_get.add_argument("--steps", action="store_true", help="Print build action step names + log URLs")
    b_get.add_argument("--step-logs", action="store_true", help="Fetch step log URL(s) and print tail")
    b_get.add_argument("--tail", type=int, default=80, help="Tail N lines when printing step logs")
    b_get.add_argument("--step-index", type=int, help="1-based step index for --step-logs")
    b_get.add_argument("--step-name-contains", help="Substring match for --step-logs")
    b_get.set_defaults(func=cmd_builds_get)

    b_cancel = builds_sub.add_parser("cancel", help="Cancel a build")
    b_cancel.add_argument("--build-id", required=True)
    b_cancel.set_defaults(func=cmd_builds_cancel)

    b_cancel_running = builds_sub.add_parser("cancel-running", help="Cancel running/queued builds")
    b_cancel_running.add_argument("--app-id")
    b_cancel_running.add_argument("--workflow-id")
    b_cancel_running.add_argument("--limit", type=int, default=20)
    b_cancel_running.add_argument("--yes", action="store_true")
    b_cancel_running.set_defaults(func=cmd_builds_cancel_running)

    b_start = builds_sub.add_parser("start", help="Start a new build")
    b_start.add_argument("--app-id", required=True)
    b_start.add_argument("--workflow-id", required=True)
    b_start.add_argument("--branch")
    b_start.add_argument("--tag")
    b_start.add_argument("--extra-json", help="Path to JSON file merged into the start payload")
    b_start.set_defaults(func=cmd_builds_start)

    b_fail = builds_sub.add_parser("failures", help="Summarize failed builds")
    b_fail.add_argument("--app-id")
    b_fail.add_argument("--workflow-id")
    b_fail.add_argument("--status", help="Override failure status string")
    b_fail.add_argument("--limit", type=int, default=20)
    b_fail.add_argument("--output", choices=["json", "text"], default="text")
    b_fail.set_defaults(func=cmd_builds_failures)

    dash = sub.add_parser("dashboard", help="Environment × platform dashboard from a matrix JSON")
    dash.add_argument("--matrix", required=True)
    dash.add_argument("--output", choices=["json", "text"], default="text")
    dash.set_defaults(func=cmd_dashboard)

    apps = sub.add_parser("apps", help="App metadata and env var management")
    apps_sub = apps.add_subparsers(dest="apps_cmd", required=True)

    a_list = apps_sub.add_parser("list", help="List apps (id + name)")
    a_list.add_argument("--output", choices=["json", "text"], default="text")
    a_list.set_defaults(func=cmd_apps_list)

    a_vars = apps_sub.add_parser("vars", help="Manage app environment variables")
    a_vars_sub = a_vars.add_subparsers(dest="vars_cmd", required=True)

    a_vars_list = a_vars_sub.add_parser("list", help="List env vars for an app")
    a_vars_list.add_argument("--app-id", required=True)
    a_vars_list.add_argument("--output", choices=["json", "text"], default="text")
    a_vars_list.set_defaults(func=cmd_apps_vars_list)

    a_vars_add = a_vars_sub.add_parser("add", help="Add an env var to an app")
    a_vars_add.add_argument("--app-id", required=True)
    a_vars_add.add_argument("--group", required=True)
    a_vars_add.add_argument("--key", required=True)
    a_vars_add.add_argument("--value", required=True)
    a_vars_add.add_argument("--secure", action="store_true")
    a_vars_add.set_defaults(func=cmd_apps_vars_add)

    a_vars_del = a_vars_sub.add_parser("delete", help="Delete an env var from an app")
    a_vars_del.add_argument("--app-id", required=True)
    a_vars_del.add_argument("--var-id", required=True)
    a_vars_del.set_defaults(func=cmd_apps_vars_delete)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
