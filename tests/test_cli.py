# tests/cli_tests.py

from typer.testing import CliRunner

from expense_tracker import __app_name__, __version__
from expense_tracker.cli import CLI


runner: CliRunner = CliRunner()


def test_version() -> None:

    result = runner.invoke(CLI.app, ["--version"])

    assert result.exit_code == 0
    assert f"{__app_name__} {__version__}" in result.stdout
