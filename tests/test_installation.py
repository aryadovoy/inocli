import sys


def test_python_version() -> None:
    assert sys.version_info >= (3, 10), (
        f"Python {sys.version_info} is not supported"
    )


def test_client_import() -> None:
    from inocli import InoreaderClient

    assert InoreaderClient is not None
