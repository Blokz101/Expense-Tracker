# expense_tracker/orm/location.py

from expense_tracker.orm import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from typing import List, Tuple, Optional

from geopy.distance import geodesic


class Merchant_Location(Base):
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
    merchant: Mapped["Merchant"] = relationship(
        back_populates="merchant_locations",
    )

    @staticmethod
    def possible_location(
        target_coord: Tuple[float, float],
        compare_coords_list: List[Tuple[float, float]],
        same_location__mile_radius: float,
    ) -> Optional[int]:
        """
        Check if a location is close enough, to any coordinate in a provided list, to be the same location. If so return the first index of such a coordinate.
        """

        # Check if each coordinate in compare_coords_list is within the specified radius of target_coord
        for index, compare_coord in enumerate(compare_coords_list):
            distance: float = geodesic(compare_coord, target_coord).miles

            # If it is then return the index of the match
            if distance <= same_location__mile_radius:
                return index

        # Return None if no matches are found
        return None
