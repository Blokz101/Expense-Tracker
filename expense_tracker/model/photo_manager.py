# expense_tracker/model/photo_coords.py

from typing import Tuple

from exif import Image

from pathlib import Path


class Photo_Manager:
    """
    Functions to manage and interact with photos
    """

    @staticmethod
    def get_coords(path: Path) -> tuple[float, float]:
        """
        Gets coords from photo and returns them as a tuple
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            if not image.has_exif:
                AttributeError("Image does not have exif data.")

            return (
                Photo_Manager._to_decimal_coords(
                    image.gps_latitude, image.gps_latitude_ref
                ),
                Photo_Manager._to_decimal_coords(
                    image.gps_longitude, image.gps_longitude_ref
                ),
            )

    @staticmethod
    def _to_decimal_coords(coords: Tuple[float, float], ref: str):
        """
        Convert coords and ref to decimal degrees format
        """

        decimal_degrees: float = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees

    @staticmethod
    def get_description(path: Path) -> str:
        """
        Get the description from the photo
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            # Check if the image has any exif data at all
            if not image.has_exif:
                raise AttributeError("Image does not have exif data.")

            # Return the image description if there is one
            return image.image_description
