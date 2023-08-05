# expense_tracker/__main__.py

from expense_tracker import __app_name__

from expense_tracker.view_controller.exptrack_app import Exptrack_App


def main() -> None:
    Exptrack_App().run()


if __name__ == "__main__":
    main()
