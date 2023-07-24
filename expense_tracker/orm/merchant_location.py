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
        coords_list: List[Tuple[float, float]],
        same_location__mile_radius: float,
    ) -> Optional[Tuple[float, float]]:
        """
        Check if a location is close enough, to any coordinate in a provided list, to be the same location. If so return the first index of such a coordinate.
        """
        
        # If the coords are within the specified radius, add it to the result list along with its distance.
        compared_coords_list: List[Tuple[float, Tuple[float, float]]] = []
        for coord in coords_list:
            distance: float = geodesic(coord, target_coord).miles
            if distance <= same_location__mile_radius:
                compared_coords_list.append((coord, distance))

        # If there are no matches, return none
        if len(compared_coords_list) == 0:
            return None

        # If there are matches, sort the list by distance and return the closest coords
        compared_coords_list.sort(key=lambda x: x[1])
        return compared_coords_list[0][0]
