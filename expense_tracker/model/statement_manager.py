# expense_tracker/model/statement_manager.py

import csv

from dataclasses import dataclass

from datetime import datetime

from pathlib import Path

from typing import Optional

from sqlalchemy.orm import Session

from expense_tracker.constants import Constants

from expense_tracker.model.db_util import DB_Util

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


@dataclass
class ST_Transaction:
    row_id: int
    description: str
    merchant: Optional[DB_Merchant]
    date: datetime
    amount: float


class Statement:
    """
    Bank statement ORM
    """

    def __init__(self, statement_path: Path, account_id: int) -> None:
        """
        Initializes the class.

        Args:
            statement_path: Path to statement.
            account_id: ID of the account that the statement belongs to.
        """

        if not statement_path.suffix == ".csv":
            raise ValueError("Statement file must be a .csv file")

        self.statement_path: Path = statement_path

        with Session(engine) as session:
            self.account: DB_Account = (
                session.query(DB_Account).where(DB_Account.id == account_id).first()
            )
            self._description_column_index: int = (
                self.account.statement_description_column_index
            )
            self._amount_column_index: int = self.account.statement_amount_column_index
            self._date_column_index: int = self.account.statement_date_column_index

        self._max_required_index: int = max(
            self._description_column_index,
            self._amount_column_index,
            self._date_column_index,
        )

    def get_all(self) -> list[ST_Transaction]:
        """
        Get a list of all the readable rows in the statement.

        Return: List of readable rows in ST_Transaction format.
        """

        st_trans_list: list[ST_Transaction] = []

        with open(self.statement_path) as statement_file:
            csv_parser: csv = csv.reader(statement_file, delimiter=",")
            for index, row in enumerate(csv_parser):
                if not self._valid_statement_row(row):
                    continue

                st_trans_list.append(
                    ST_Transaction(
                        index,
                        row[self._description_column_index],
                        DB_Util.get_merchant_from_description(
                            row[self._description_column_index]
                        ),
                        datetime.strptime(
                            row[self._date_column_index],
                            Constants.STATEMENT_DATE_FORMAT,
                        ),
                        float(row[self._amount_column_index]),
                    )
                )

        return st_trans_list

    def _valid_statement_row(self, row: tuple[str, ...]) -> bool:
        """
        Check if the row is readable.

        Args:
            row: Tuple containing the row info.

        Return: True if row is valid false if not.
        """
        if len(row) - 1 < self._max_required_index:
            return False

        try:
            float(row[self._amount_column_index])
        except ValueError:
            return False

        if not self._valid_date(row[self._date_column_index]):
            return False

        return True

    def _valid_date(self, date: str) -> bool:
        """
        Checks if the date can be read.

        Args:
            date: Input string to be validated.

        Return: True if date can be read and false if not.
        """
        try:
            datetime.strptime(date, Constants.STATEMENT_DATE_FORMAT)
            return True
        except ValueError:
            return False
