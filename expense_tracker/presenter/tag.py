# expense_tracker/presenter/tag.py

from sqlalchemy.orm import Session

from datetime import datetime

from enum import Enum

from typing import Union

from expense_tracker.constants import Constants

from expense_tracker.presenter.presenter import Presenter

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_transaction import DB_Transaction
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Tag(Presenter):
    """
    Tag presenter
    """

    class Column(Enum):
        ID: int = 0
        NAME: int = 1
        INSTANCE_TAG: int = 2

    @staticmethod
    def _format(tag: DB_Tag) -> tuple[int, ...]:
        """
        Formats raw database tags into a tuple
        """

        return (
            tag.id,
            tag.name,
            str(tag.instance_tag),
        )

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all tags as a list of tuples of strings
        """

        with Session(engine) as session:
            return list(Tag._format(tag) for tag in session.query(DB_Tag).all())

    @staticmethod
    def get_by_id(id: int) -> list[tuple[int, ...]]:
        """
        Returns a single object with the requested id
        """
        with Session(engine) as session:
            return Tag._format(session.query(DB_Tag).where(DB_Tag.id == id).first())

    @staticmethod
    def create(values: dict[Enum, Union[int, str, datetime]]) -> tuple[int, ...]:
        """
        Create a transaction
        """

        with Session(engine) as session:
            new_tag: DB_Tag = DB_Tag(
                name=values[Tag.Column.NAME],
                instance_tag=values[Tag.Column.INSTANCE_TAG],
            )
            session.add(new_tag)
            session.commit()
            return Tag._format(new_tag)

    @staticmethod
    def set_value(id: int, column: Column, new_value: Union[int, str, datetime]) -> str:
        """
        Updates cell in the database
        """
        with Session(engine) as session:
            tag: DB_Tag = session.query(DB_Tag).where(DB_Tag.id == id).first()

            # new_value will be an str
            if column == Tag.Column.NAME:
                tag.name = new_value
                session.commit()
                return tag.name

            # new_value will be a bool
            if column == Tag.Column.INSTANCE_TAG:
                tag.instance_tag = new_value
                session.commit()
                return tag.instance_tag

        Presenter.set_value(id, column, new_value)

    # TODO Edit this entire method to work with multiple amounts
    @staticmethod
    def get_tags_for_transaction(id: int) -> list[tuple[int, ...]]:
        """
        Gets the tags from the first amount that a transaction has
        """

        with Session(engine) as session:
            transaction: DB_Transaction = (
                session.query(DB_Transaction).where(DB_Transaction.id == id).first()
            )
            amount: DB_Amount = (
                session.query(DB_Amount).where(DB_Amount.id == transaction.id).first()
            )
            tag_list: list[DB_Tag] = (
                session.query(DB_Tag).where(DB_Tag.amounts.contains(amount)).all()
            )

            return list(Tag._format(tag) for tag in tag_list)

    @staticmethod
    def get_tags_for_merchant_default(merchant_id: int) -> list[tuple[int, ...]]:
        """
        Get a list of tag ids that are the defaults for a merchant
        """

        with Session(engine) as session:
            merchant: DB_Merchant = (
                session.query(DB_Merchant).where(DB_Merchant.id == merchant_id).first()
            )
            return list(Tag._format(tag) for tag in merchant.default_tags)

    @staticmethod
    def get_value(value: Union[int, str, datetime], column: Column) -> str:
        """
        Format or get a value based on the column it was requested for
        """

        # value will be a str
        if column == Tag.Column.NAME or column == Tag.Column.INSTANCE_TAG:
            return str(value)

        return Presenter.get_value(id, column)

    @staticmethod
    def get_tag_list(tag_id_list: list[int]) -> list[DB_Tag]:
        """
        Convert a list of tag ids to a list of tags
        """

        with Session(engine) as session:
            return list(
                session.query(DB_Tag).where(DB_Tag.id == tag_id).first()
                for tag_id in tag_id_list
            )
