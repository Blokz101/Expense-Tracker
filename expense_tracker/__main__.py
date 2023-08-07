# expense_tracker/__main__.py

from expense_tracker import __app_name__

from expense_tracker.view.exptrack_app import Exptrack_App


def main() -> None:
    app: Exptrack_App = Exptrack_App()
    app.run()


if __name__ == "__main__":
    main()
