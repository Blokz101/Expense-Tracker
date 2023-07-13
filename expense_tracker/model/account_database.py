# expense_tracker/model/account_database.py

from sqlalchemy.orm import Session

from expense_tracker.orm import engine
from expense_tracker.orm.merchant import Merchant
from expense_tracker.orm.amount import Amount
from expense_tracker.orm.merchant_location import Merchant_Location
from expense_tracker.orm.transaction import Transaction
from expense_tracker.orm.tag import Tag
from expense_tracker.orm.account import Account


class Account_Database:
    """
    Account sub commands
    """

    @staticmethod
    def create(name: str) -> None:
        """
        Create a new account.
        """

        with Session(engine) as session:
            session.add(Account(name=name))
            session.commit()

    @staticmethod
    def get_all() -> list:
        """
        List all accounts in database
        """

        with Session(engine) as session:
            return session.query(Account).all()

    @staticmethod
    def get_filterd_by_name(filter: str) -> list:
        """
        List accounts in database filtered by name.
        """

        with Session(engine) as session:
            return (
                session.query(Account).filter(Account.name.like(f"%{filter}%")).all()
            )

    @staticmethod
    def delete(account: Account) -> None:
        """
        Delete a account in database.
        """

        with Session(engine) as session:
            session.delete(account)
            session.commit()
            
    @staticmethod
    def rename(account: Account, new_name: str) -> None:
        """
        Renames a account in the database.
        """
        
        with Session(engine) as session:
            session.add(account)
            account.name = new_name
            session.commit()
