"""Local development HTTP server for the Pollen app shell."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable
from urllib.parse import parse_qs, urlsplit

from pollen.app import AppResponse, AppShell, create_app

DEMO_AUTH_HEADER = "Bearer user:local-demo:local-demo@example.com"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
_HTML_CONTENT_TYPE = "text/html; charset=utf-8"
_TEXT_CONTENT_TYPE = "text/plain; charset=utf-8"


@dataclass(frozen=True)
class HttpResponse:
    """HTTP response data produced by the dev-server adapter."""

    status_code: int
    body: bytes
    headers: dict[str, str] = field(default_factory=dict)


class DevServerAdapter:
    """Adapt standard-library HTTP requests to the existing app-shell API."""

    def __init__(self, app: AppShell | None = None, *, demo_auth_header: str = DEMO_AUTH_HEADER) -> None:
        self._app = app or create_app()
        self._demo_auth_header = demo_auth_header

    def handle_get(self, path: str) -> HttpResponse:
        if self._is_health_check_path(path):
            return self._plain_response(HTTPStatus.OK, "OK")

        app_response = self._app.get(path, authorization_header=self._demo_auth_header)
        return self._to_http_response(app_response)

    def handle_head(self, path: str) -> HttpResponse:
        response = self.handle_get(path)
        return HttpResponse(
            status_code=response.status_code,
            body=b"",
            headers=response.headers,
        )

    def handle_post(
        self,
        path: str,
        *,
        body: bytes,
        content_type: str | None,
    ) -> HttpResponse:
        route_path = urlsplit(path).path
        if not self._is_supported_form_content_type(content_type):
            return self._plain_response(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "Unsupported Media Type",
            )

        form_data = self._parse_form_data(body)
        app_response = self._app.post(
            route_path,
            authorization_header=self._demo_auth_header,
            form_data=form_data,
        )
        return self._to_http_response(app_response)

    def handle_unsupported_method(self) -> HttpResponse:
        return self._plain_response(HTTPStatus.METHOD_NOT_ALLOWED, "Method Not Allowed")

    def _parse_form_data(self, body: bytes) -> dict[str, str]:
        decoded_body = body.decode("utf-8")
        parsed = parse_qs(decoded_body, keep_blank_values=True)
        return {key: values[-1] if values else "" for key, values in parsed.items()}

    def _to_http_response(self, app_response: AppResponse) -> HttpResponse:
        return HttpResponse(
            status_code=app_response.status_code,
            body=app_response.body.encode("utf-8"),
            headers={"Content-Type": _HTML_CONTENT_TYPE},
        )

    def _plain_response(self, status: HTTPStatus, body: str) -> HttpResponse:
        return HttpResponse(
            status_code=status.value,
            body=body.encode("utf-8"),
            headers={"Content-Type": _TEXT_CONTENT_TYPE},
        )

    def _is_supported_form_content_type(self, content_type: str | None) -> bool:
        if content_type is None:
            return True
        media_type = content_type.split(";", maxsplit=1)[0].strip().lower()
        return media_type in {"", "application/x-www-form-urlencoded"}

    def _is_health_check_path(self, path: str) -> bool:
        return urlsplit(path).path == "/healthz"


class PollenDevRequestHandler(BaseHTTPRequestHandler):
    """Small local-only request handler for browsing the app shell."""

    server_version = "PollenDevServer/1.0"

    def do_GET(self) -> None:  # noqa: N802
        self._send_response(self._adapter.handle_get(self.path))

    def do_HEAD(self) -> None:  # noqa: N802
        self._send_response(self._adapter.handle_head(self.path))

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(content_length) if content_length > 0 else b""
        self._send_response(
            self._adapter.handle_post(
                self.path,
                body=body,
                content_type=self.headers.get("Content-Type"),
            )
        )

    def do_PUT(self) -> None:  # noqa: N802
        self._send_response(self._adapter.handle_unsupported_method())

    def do_DELETE(self) -> None:  # noqa: N802
        self._send_response(self._adapter.handle_unsupported_method())

    def do_PATCH(self) -> None:  # noqa: N802
        self._send_response(self._adapter.handle_unsupported_method())

    @property
    def _adapter(self) -> DevServerAdapter:
        return self.server.adapter  # type: ignore[attr-defined]

    def _send_response(self, response: HttpResponse) -> None:
        self.send_response(response.status_code)
        for header, value in response.headers.items():
            self.send_header(header, value)
        self.send_header("Content-Length", str(len(response.body)))
        self.end_headers()
        self.wfile.write(response.body)

    def log_message(self, format: str, *args: object) -> None:
        """Keep local server logging concise and compatible with BaseHTTPRequestHandler."""
        print(f"{self.address_string()} - {format % args}")


class PollenDevServer(ThreadingHTTPServer):
    """Threaded local HTTP server carrying the Pollen app adapter."""

    def __init__(
        self,
        server_address: tuple[str, int],
        handler_class: type[BaseHTTPRequestHandler] = PollenDevRequestHandler,
        *,
        adapter: DevServerAdapter | None = None,
    ) -> None:
        super().__init__(server_address, handler_class)
        self.adapter = adapter or DevServerAdapter()


def create_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    *,
    app_factory: Callable[[], AppShell] = create_app,
) -> PollenDevServer:
    """Create the local dev server without starting its serving loop."""
    return PollenDevServer((host, port), adapter=DevServerAdapter(app_factory()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local Pollen app-shell development server.")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host to bind, default: {DEFAULT_HOST}")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to bind, default: {DEFAULT_PORT}")
    args = parser.parse_args(argv)

    server = create_server(args.host, args.port)
    url_host = "localhost" if args.host in {"", "0.0.0.0", DEFAULT_HOST} else args.host
    print(f"Pollen local dev server running at http://{url_host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Pollen local dev server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
