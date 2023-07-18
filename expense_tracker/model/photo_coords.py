# expense_tracker/model/photo_coords.py

import exif
from exif import Image

from pathlib import Path


class Coords_Manager:
    """
    Gets coordinates from photo
    """

    @staticmethod
    def get_coords_from_photo(path: Path) -> tuple[float, float]:
        """
        Gets coords from photo and returns them as a tuple
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            if not image.has_exif:
                AttributeError("Image does not have exif data.")

            return (
                Coords_Manager.decimal_coords(image.gps_latitude, image.gps_latitude_ref),
                Coords_Manager.decimal_coords(
                    image.gps_longitude, image.gps_longitude_ref
                ),
            )

    @staticmethod
    def decimal_coords(coords, ref):
        """
        Convert coords and ref to decimal degrees format
        """

        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees
