# expense_tracker/presenter/merchant.py

from sqlalchemy.orm import Session

from enum import Enum

from datetime import datetime

from typing import Union

from expense_tracker.presenter.presenter import Presenter
from expense_tracker.presenter.tag import Tag

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Merchant(Presenter):
    """
    Merchant presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        NAMING_RULE: int = 2
        DEFAULT_TAGS: int = 3

    @staticmethod
    def _format(merchant: DB_Merchant) -> tuple[int, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            merchant.id,
            merchant.name,
            merchant.naming_rule,
            ", ".join(tag.name for tag in merchant.default_tags),
        )

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return list(
                Merchant._format(merchant)
                for merchant in session.query(DB_Merchant).all()
            )

    @staticmethod
    def get_by_id(id: int) -> list[tuple[int, ...]]:
        """
        Returns a single object with the requested id
        """
        with Session(engine) as session:
            return Merchant._format(
                session.query(DB_Merchant).where(DB_Merchant.id == id).first()
            )

    @staticmethod
    def create(values: dict[Enum, Union[int, str, datetime]]) -> tuple[int, ...]:
        """
        Create a merchant
        """

        with Session(engine) as session:
            new_merchant: DB_Merchant = DB_Merchant(
                name=values[Merchant.Column.NAME],
                naming_rule=values[Merchant.Column.NAMING_RULE],
            )
            session.add(new_merchant)
            session.commit()
            return Merchant._format(new_merchant)

    @staticmethod
    def set_value(id: int, column: Column, new_value: Union[int, str, datetime]) -> str:
        """
        Updates cell in the database
        """
        with Session(engine) as session:
            merchant: DB_Merchant = (
                session.query(DB_Merchant).where(DB_Merchant.id == id).first()
            )

            # new_value will be an str
            if column == Merchant.Column.NAME:
                merchant.name = new_value
                session.commit()
                return merchant.name

            # new_value will be an str
            if column == Merchant.Column.NAMING_RULE:
                merchant.naming_rule = new_value
                session.commit()
                return merchant.naming_rule

            # new_value will be a list of ints representing ids of tags
            if column == Merchant.Column.DEFAULT_TAGS:
                merchant.default_tags = []
                for id in new_value:
                    tag: DB_Tag = session.query(DB_Tag).where(DB_Tag.id == id).first()
                    merchant.default_tags.append(tag)
                session.commit()
                return ", ".join(tag.name for tag in merchant.default_tags)

        Presenter.set_value(id, column, new_value)

    @staticmethod
    def get_value(value: Union[int, str, datetime], column: Column) -> str:
        """
        Format or get a value based on the column it was requested for
        """

        # value will be a str
        if column == Merchant.Column.NAME or column == Merchant.Column.NAMING_RULE:
            return str(value)

        with Session(engine) as session:
            # value will be a list of ints
            # TODO Edit this to support multiple amounts
            if column == Merchant.Column.DEFAULT_TAGS:
                return ", ".join(tag.name for tag in Tag.get_tag_list(value))

        return Presenter.get_value(id, column)
