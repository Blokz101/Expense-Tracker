# expense_tracker/__main__.py

from expense_tracker import __app_name__

from expense_tracker.model.orm import engine, Base
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget

from expense_tracker.config_manager import Config_Manager

import os

from expense_tracker.view.exptrack_app import Exptrack_App


def main() -> None:
    if not os.path.exists(Config_Manager().get_database_path()):
        Base.metadata.create_all(engine)

    app: Exptrack_App = Exptrack_App()
    app.run()


if __name__ == "__main__":
    main()
