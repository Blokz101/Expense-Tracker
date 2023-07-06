# expense_tracker/__main__.py

from expense_tracker import __app_name__
from expense_tracker.cli import CLI


def main() -> None:
    CLI.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
