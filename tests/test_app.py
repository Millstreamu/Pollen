from pollen.app import healthcheck


def test_healthcheck_payload() -> None:
    assert healthcheck() == {"status": "ok", "service": "pollen"}
