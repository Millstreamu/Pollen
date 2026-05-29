from http import HTTPStatus
from urllib.parse import urlencode

import pytest

from pollen.dev_server import DevServerAdapter, create_server, main


def test_dev_server_adapter_get_today_page_uses_demo_auth() -> None:
    response = DevServerAdapter().handle_get("/")

    assert response.status_code == HTTPStatus.OK
    assert b"<h1>Today</h1>" in response.body
    assert b"Today summary" in response.body
    assert response.headers["Content-Type"].startswith("text/html")


def test_dev_server_adapter_get_health_check_is_plain_ok() -> None:
    response = DevServerAdapter().handle_get("/healthz")

    assert response.status_code == HTTPStatus.OK
    assert response.body == b"OK"
    assert response.headers["Content-Type"].startswith("text/plain")


def test_dev_server_adapter_head_health_check_returns_headers_without_body() -> None:
    response = DevServerAdapter().handle_head("/healthz")

    assert response.status_code == HTTPStatus.OK
    assert response.body == b""
    assert response.headers["Content-Type"].startswith("text/plain")


def test_dev_server_adapter_get_navigation_routes() -> None:
    adapter = DevServerAdapter()

    for path, expected_heading in [
        ("/orders", b"<h1>Orders</h1>"),
        ("/products-stock", b"<h1>Products & Stock</h1>"),
        ("/make-buy", b"<h1>Make / Buy</h1>"),
        ("/money", b"<h1>Money</h1>"),
        ("/settings", b"<h1>Settings</h1>"),
    ]:
        response = adapter.handle_get(path)
        assert response.status_code == HTTPStatus.OK
        assert expected_heading in response.body


def test_dev_server_adapter_post_form_uses_app_shell_logic() -> None:
    adapter = DevServerAdapter()
    payload = urlencode(
        {
            "action": "create",
            "name": "Browser Candle",
            "sku": "BROWSER-001",
            "stock_on_hand": "6",
            "reorder_point": "2",
        }
    ).encode("utf-8")

    response = adapter.handle_post(
        "/products-stock",
        body=payload,
        content_type="application/x-www-form-urlencoded",
    )

    assert response.status_code == HTTPStatus.OK
    assert b"Browser Candle" in response.body
    assert b"BROWSER-001" in response.body


def test_dev_server_adapter_returns_not_found_for_unknown_path() -> None:
    response = DevServerAdapter().handle_get("/missing")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert b"Not Found" in response.body


def test_dev_server_adapter_rejects_unsupported_post_content_type() -> None:
    response = DevServerAdapter().handle_post(
        "/products-stock",
        body=b"{}",
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    assert b"Unsupported Media Type" in response.body


def test_dev_server_adapter_rejects_unsupported_methods() -> None:
    response = DevServerAdapter().handle_unsupported_method()

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert b"Method Not Allowed" in response.body


def test_create_server_uses_requested_ephemeral_port() -> None:
    server = create_server(port=0)
    try:
        assert server.server_address[1] != 0
        assert server.adapter.handle_get("/").status_code == HTTPStatus.OK
    finally:
        server.server_close()


def test_main_help_exits_successfully(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "Run the local Pollen app-shell development server." in captured.out
