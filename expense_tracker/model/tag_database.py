# expense_tracker/model/tag_database.py

from typing import List

from sqlalchemy.orm import Session

from expense_tracker.model import engine
from expense_tracker.model.merchant import Merchant
from expense_tracker.model.amount import Amount
from expense_tracker.model.merchant_location import Merchant_Location
from expense_tracker.model.transaction import Transaction
from expense_tracker.model.tag import Tag
from expense_tracker.model.account import Account


class Tag_Database:
    """
    Tag sub commands
    """

    @staticmethod
    def create(name: str) -> None:
        """
        Create a new tag.
        """

        with Session(engine) as session:
            session.add(Tag(name=name))
            session.commit()

    @staticmethod
    def get_all() -> list:
        """
        List all tags in database
        """

        with Session(engine) as session:
            return session.query(Tag).all()

    @staticmethod
    def get_filterd_by_name(filter: str) -> list:
        """
        List tags in database filtered by name.
        """

        with Session(engine) as session:
            return (
                session.query(Tag).filter(Tag.name.like(f"%{filter}%")).all()
            )

    @staticmethod
    def delete(tag: Tag) -> None:
        """
        Delete a tag in database.
        """

        with Session(engine) as session:
            session.delete(tag)
            session.commit()
            
    @staticmethod
    def rename(tag: Tag, new_name: str) -> None:
        """
        Renames a tag in the database.
        """
        
        with Session(engine) as session:
            session.add(tag)
            tag.name = new_name
            session.commit()
