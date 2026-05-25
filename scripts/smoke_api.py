from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 5


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def get_json(path: str) -> tuple[int, Any]:
    request = Request(f"{BASE_URL}{path}", method="GET")
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            payload = json.loads(body) if body else None
            return response.status, payload
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        payload = json.loads(body) if body else None
        return exc.code, payload
    except URLError as exc:
        raise RuntimeError(f"Could not reach {BASE_URL}: {exc.reason}") from exc


def check(name: str, path: str, expected_status: int = 200) -> CheckResult:
    status, _ = get_json(path)
    if status == expected_status:
        return CheckResult(name, True, f"{status} {path}")
    return CheckResult(name, False, f"expected {expected_status}, got {status} for {path}")


def main() -> int:
    results: list[CheckResult] = []

    try:
        status, health = get_json("/health")
        results.append(
            CheckResult(
                "health",
                status == 200 and health == {"status": "ok"},
                f"{status} /health",
            )
        )

        status, applications = get_json("/api/applications")
        applications_ok = status == 200 and isinstance(applications, list) and len(applications) > 0
        results.append(CheckResult("applications list", applications_ok, f"{status} /api/applications"))

        first_application_id = None
        if applications_ok:
            first_application = applications[0]
            if isinstance(first_application, dict):
                first_application_id = first_application.get("id")

        if not isinstance(first_application_id, str) or not first_application_id:
            results.append(CheckResult("first application id", False, "missing id"))
        else:
            results.append(check("application detail", f"/api/applications/{first_application_id}"))
            results.append(
                check(
                    "interview packet",
                    f"/api/applications/{first_application_id}/interview-packet",
                )
            )
            results.append(check("gaps", f"/api/applications/{first_application_id}/gaps"))

        results.append(check("evidence", "/api/evidence"))
        results.append(check("dashboard summary", "/api/dashboard/summary"))
        results.append(check("prep actions", "/api/dashboard/prep-actions"))

        unknown = "unknown-application-id"
        results.append(check("unknown detail 404", f"/api/applications/{unknown}", 404))
        results.append(
            check(
                "unknown interview packet 404",
                f"/api/applications/{unknown}/interview-packet",
                404,
            )
        )
        results.append(check("unknown gaps 404", f"/api/applications/{unknown}/gaps", 404))
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1

    failures = [result for result in results if not result.passed]
    for result in results:
        label = "PASS" if result.passed else "FAIL"
        print(f"{label}: {result.name} - {result.detail}")

    if failures:
        print(f"\nSmoke API result: FAIL ({len(failures)} failed, {len(results)} checked)")
        return 1

    print(f"\nSmoke API result: PASS ({len(results)} checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
