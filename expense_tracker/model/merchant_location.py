# expense_tracker/model/location.py

from expense_tracker.model import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column


class Merchant_Location(Base):
    """ """

    __tablename__ = "merchant_locations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("merchants.id"),
        unique=True,
        nullable=False,
    )
    x_coord: Mapped[float] = mapped_column(
        nullable=False,
    )
    y_coord: Mapped[float] = mapped_column(
        nullable=False,
    )

    merchant: Mapped["Merchant"] = relationship(
        back_populates="merchant_locations",
    )
