# expense_tracker/model/photo_coords.py

from exif import Image

from pathlib import Path

from expense_tracker.model.coords_utils import Coords_Utils


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
                Coords_Utils.decimal_coords(image.gps_latitude, image.gps_latitude_ref),
                Coords_Utils.decimal_coords(
                    image.gps_longitude, image.gps_longitude_ref
                ),
            )

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
