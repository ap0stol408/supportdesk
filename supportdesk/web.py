import json
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import parse_qs, urlsplit

from supportdesk.auth import SessionRegistry
from supportdesk.config import Settings
from supportdesk.diagnostics import snapshot
from supportdesk.reports import export_report
from supportdesk.service import IssueService
from supportdesk.templates import render_issue


@dataclass(frozen=True)
class Response:
    status: int
    body: bytes
    content_type: str = "application/json; charset=utf-8"


def json_response(status: int, value: object) -> Response:
    return Response(status, json.dumps(value).encode("utf-8"))


class Application:
    def __init__(self, settings: Settings, sessions: SessionRegistry) -> None:
        self.settings = settings
        self.sessions = sessions
        self.issues = IssueService(settings.database)

    def handle(
        self, method: str, target: str, headers: Mapping[str, str], body: bytes = b""
    ) -> Response:
        try:
            return self._dispatch(method, target, headers, body)
        except (ValueError, UnicodeError, sqlite3.Error):
            return json_response(400, {"error": "Invalid request"})

    def _dispatch(
        self, method: str, target: str, headers: Mapping[str, str], body: bytes
    ) -> Response:
        url = urlsplit(target)
        parameters = parse_qs(url.query)
        if method == "GET" and url.path == "/health":
            return json_response(200, {"status": "ok"})
        user_id = self.sessions.resolve(headers)
        if user_id is None:
            return json_response(401, {"error": "Authentication required"})
        if method == "GET" and url.path.startswith("/issues/"):
            issue_id = int(url.path.removeprefix("/issues/"))
            issue = self.issues.get(issue_id)
            if issue is None:
                return json_response(404, {"error": "Ticket not found"})
            page = render_issue(issue)
            return Response(200, page.encode("utf-8"), "text/html; charset=utf-8")
        if method == "GET" and url.path == "/api/debug":
            return json_response(200, snapshot())
        if method == "GET" and url.path == "/api/reports":
            format_name = parameters.get("format", ["csv"])[0]
            output = export_report(format_name, self.settings.database.parent)
            return json_response(200, {"output": output})
        if method == "GET" and url.path == "/api/issues":
            query = parameters.get("q", [""])[0]
            return json_response(200, {"issues": self.issues.search(user_id, query)})
        if method == "POST" and url.path == "/api/issues":
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("Expected an object")
            title, content = data.get("title"), data.get("body", "")
            if not isinstance(title, str) or not isinstance(content, str):
                raise ValueError("Expected text")
            issue_id = self.issues.create(user_id, title, content)
            return json_response(201, {"id": issue_id})
        if method == "GET" and url.path.startswith("/api/issues/"):
            issue_id = int(url.path.removeprefix("/api/issues/"))
            issue = self.issues.get(issue_id)
            if issue is None:
                return json_response(404, {"error": "Ticket not found"})
            return json_response(200, issue)
        return json_response(404, {"error": "Route not found"})
