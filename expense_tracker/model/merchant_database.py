# expense_tracker/model/merchant_database.py

from sqlalchemy.orm import Session

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account


class Merchant_Database:
    """
    Merchant sub commands
    """

    @staticmethod
    def create(name: str) -> None:
        """
        Create a new merchant.
        """

        with Session(engine) as session:
            session.add(Merchant(name=name))
            session.commit()

    @staticmethod
    def get_all() -> list:
        """
        List all merchants in database
        """

        with Session(engine) as session:
            return session.query(Merchant).all()

    @staticmethod
    def get_filterd_by_name(filter: str) -> list:
        """
        List merchants in database filtered by name.
        """

        with Session(engine) as session:
            return (
                session.query(Merchant).filter(Merchant.name.like(f"%{filter}%")).all()
            )

    @staticmethod
    def delete(merchant: Merchant) -> None:
        """
        Delete a merchant in database.
        """

        with Session(engine) as session:
            session.delete(merchant)
            session.commit()
            
    @staticmethod
    def rename(merchant: Merchant, new_name: str) -> None:
        """
        Renames a merchant in the database.
        """
        
        with Session(engine) as session:
            session.add(merchant)
            merchant.name = new_name
            session.commit()
