# expense_tracker/model/branch_table.py

from expense_tracker.model import Base

from sqlalchemy import Table, Column, ForeignKey


class Branch_Table:
    """
    Association tables for the various tables that require a many to many connection
    """

    transaction_tag: Table = Table(
        "transaction_tag_branches",
        Base.metadata,
        Column("transaction_id", ForeignKey("transactions.id")),
        Column("tag_id", ForeignKey("tags.id")),
    )

    merchant_tag_default: Table = Table(
        "merchant_tag_defaults",
        Base.metadata,
        Column("merchant_id", ForeignKey("merchants.id")),
        Column("tag_id", ForeignKey("tags.id")),
    )
