# expense_tracker/orm/db_location.py

from __future__ import annotations

from expense_tracker.model.orm import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class DB_Merchant_Location(Base):
    """
    SQLAlchemy merchant_locations table

    Stores merchant locations that can be assigned to a merchant.
    """

    __tablename__ = "merchant_locations"

    # Database columns
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("merchants.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        nullable=False,
    )
    x_coord: Mapped[float] = mapped_column(
        nullable=False,
    )
    y_coord: Mapped[float] = mapped_column(
        nullable=False,
    )

    # ORM objects
    merchant: Mapped["DB_Merchant"] = relationship(
        back_populates="merchant_locations",
    )

    def get_coords(self) -> tuple[float, float]:
        """
        Returns coords in a tuple object
        """

        return (self.x_coord, self.y_coord)
