"""Local web app server for Esslayit."""

from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .models import CheckConfig, Issue
from .rules import check_text

WEB_DIR = Path(__file__).resolve().parent / "webapp"
MAX_BODY_BYTES = 1_000_000


def make_check_response(text: str, max_sentence_words: int = CheckConfig.max_sentence_words) -> dict[str, object]:
    """Return a JSON-ready writing check response."""

    config = CheckConfig(max_sentence_words=max_sentence_words)
    issues = check_text(text, config)
    return {
        "issue_count": len(issues),
        "issues": [_issue_to_dict(issue) for issue in issues],
    }


class EsslayitRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler for the local Esslayit web app."""

    server_version = "EsslayitWeb/0.1"

    def do_GET(self) -> None:
        request_path = urlparse(self.path).path
        if request_path in ("/", "/index.html"):
            self._send_file(WEB_DIR / "index.html")
            return

        if request_path.startswith("/static/"):
            relative = Path(unquote(request_path.removeprefix("/static/")))
            if relative.is_absolute() or ".." in relative.parts:
                self._send_json({"error": "Invalid static file path."}, HTTPStatus.BAD_REQUEST)
                return
            self._send_file(WEB_DIR / "static" / relative)
            return

        self._send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        request_path = urlparse(self.path).path
        if request_path != "/api/check":
            self._send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json({"error": "Invalid content length."}, HTTPStatus.BAD_REQUEST)
            return

        if length > MAX_BODY_BYTES:
            self._send_json({"error": "Text is too large for the local checker."}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return

        try:
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body) if body else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json({"error": "Request body must be valid JSON."}, HTTPStatus.BAD_REQUEST)
            return

        text = payload.get("text", "")
        if not isinstance(text, str):
            self._send_json({"error": "The text field must be a string."}, HTTPStatus.BAD_REQUEST)
            return

        max_sentence_words = _safe_int(payload.get("max_sentence_words"), CheckConfig.max_sentence_words)
        max_sentence_words = max(5, min(max_sentence_words, 80))
        self._send_json(make_check_response(text, max_sentence_words))

    def log_message(self, format: str, *args: object) -> None:
        """Keep default logging, but make the type checker happy."""

        super().log_message(format, *args)

    def _send_file(self, path: Path) -> None:
        if not path.is_file():
            self._send_json({"error": "Not found."}, HTTPStatus.NOT_FOUND)
            return

        content_type, _ = mimetypes.guess_type(path.name)
        if content_type is None:
            content_type = "application/octet-stream"
        if content_type.startswith("text/") or content_type == "application/javascript":
            content_type = f"{content_type}; charset=utf-8"

        content = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, payload: dict[str, object], status: HTTPStatus = HTTPStatus.OK) -> None:
        content = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run the local web server."""

    server = ThreadingHTTPServer((host, port), EsslayitRequestHandler)
    print(f"Esslayit web app running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Esslayit web app.")
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Esslayit local web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to.")
    args = parser.parse_args(argv)
    run(args.host, args.port)
    return 0


def _issue_to_dict(issue: Issue) -> dict[str, object]:
    return {
        "rule_id": issue.rule_id,
        "severity": issue.severity,
        "message": issue.message,
        "suggestion": issue.suggestion,
        "line": issue.line,
        "column": issue.column,
        "excerpt": issue.excerpt,
    }


def _safe_int(value: object, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


if __name__ == "__main__":
    raise SystemExit(main())
