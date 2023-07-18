# expense_tracker/orm/branch_table.py

from expense_tracker.orm import Base

from sqlalchemy import Table, Column, ForeignKey


class Branch_Table:
    """
    SQLAlchemy association tables for the various tables that require a many to many connection.
    """

    amount_tag: Table = Table(
        "amount_tag_branches",
        Base.metadata,
        Column("amount_id", ForeignKey("amounts.id")),
        Column("tag_id", ForeignKey("tags.id")),
    )

    merchant_tag_default: Table = Table(
        "merchant_tag_defaults",
        Base.metadata,
        Column("merchant_id", ForeignKey("merchants.id")),
        Column("tag_id", ForeignKey("tags.id")),
    )
