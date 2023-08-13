# expense_tracker/presenter/location.py

from sqlalchemy.orm import Session

from enum import Enum

from expense_tracker.presenter.presenter import Presenter

from expense_tracker.model.orm import engine
from expense_tracker.model.orm.db_merchant import DB_Merchant
from expense_tracker.model.orm.db_amount import DB_Amount
from expense_tracker.model.orm.db_account import DB_Account
from expense_tracker.model.orm.db_merchant_location import DB_Merchant_Location
from expense_tracker.model.orm.db_tag import DB_Tag
from expense_tracker.model.orm.db_budget import DB_Budget
from expense_tracker.model.orm.db_month_budget import DB_Month_Budget


class Location(Presenter):
    """
    Location presenter
    """

    class Column(Enum):
        ID: int = 0
        MERCHANT: int = 1
        NAME: int = 2
        XCOORD: int = 3
        YCOORD: int = 4

    @staticmethod
    def _format(location: DB_Merchant_Location) -> tuple[int, ...]:
        """
        Formats raw database transaction into a tuple
        """
        return (
            location.id,
            location.merchant.name,
            location.name,
            float(location.x_coord),
            float(location.y_coord),
        )

    @staticmethod
    def get_by_id(id: int) -> list[tuple[int, ...]]:
        """
        Returns a single object with the requested id
        """
        with Session(engine) as session:
            return Location._format(
                session.query(DB_Merchant_Location)
                .where(DB_Merchant_Location.id == id)
                .first()
            )

    @staticmethod
    def create(values: dict[Enum, any]) -> tuple[int, ...]:
        """
        Create a transaction
        """

        with Session(engine) as session:
            new_location: DB_Merchant_Location = DB_Merchant_Location(
                merchant_id=values[Location.Column.MERCHANT],
                name=values[Location.Column.NAME],
                x_coord=values[Location.Column.XCOORD],
                y_coord=values[Location.Column.YCOORD],
            )
            session.add(new_location)
            session.commit()
            return Location._format(new_location)

    @staticmethod
    def get_all() -> list[tuple[int, ...]]:
        """
        Returns a list of all merchants as a list of tuples of strings
        """
        with Session(engine) as session:
            return list(
                Location._format(location)
                for location in session.query(DB_Merchant_Location).all()
            )

    @staticmethod
    def set_value(id: int, column: Column, new_value: any) -> any:
        """
        Updates cell in the database
        """
        with Session(engine) as session:
            location: DB_Merchant_Location = (
                session.query(DB_Merchant_Location)
                .where(DB_Merchant_Location.id == id)
                .first()
            )

            # new_value will be an str
            if column == Location.Column.NAME:
                location.name = new_value
                session.commit()
                return location.name

            # new_value will be an int representing the id of the new merchant
            if column == Location.Column.MERCHANT:
                new_merchant: DB_Merchant = (
                    session.query(DB_Merchant)
                    .where(DB_Merchant.id == new_value)
                    .first()
                )
                Location.merchant = new_merchant
                session.commit()
                return Location.merchant.name

            # new_value will be an str
            if column == Location.Column.XCOORD:
                location.x_coord = float(new_value)
                session.commit()
                return location.x_coord

            # new_value will be an str
            if column == Location.Column.YCOORD:
                location.y_coord = float(new_value)
                session.commit()
                return location.y_coord

        Presenter.set_value(id, column, new_value)

    @staticmethod
    def get_value(value: any, column: Column) -> any:
        """
        Format or get a value based on the column it was requested for
        """

        # value will be a str
        if column == Location.Column.NAME:
            return str(value)

        # value will be a date time object
        if column == Location.Column.XCOORD or column == Location.Column.YCOORD:
            return float(value)

        with Session(engine) as session:
            # value will be an int representing a merchant id
            if column == Location.Column.MERCHANT:
                merchant: DB_Merchant = (
                    session.query(DB_Merchant).where(DB_Merchant.id == value).first()
                )
                return merchant.name

        return Presenter.get_value(id, column)
