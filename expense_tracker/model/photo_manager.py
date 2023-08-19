# expense_tracker/model/photo_coords.py

from exif import Image

import re

from pathlib import Path

from datetime import datetime

from typing import Optional

from expense_tracker.constants import Constants

import shutil


class Photo_Manager:
    """
    Functions to manage and interact with photos
    """

    @staticmethod
    def directory_exists(dir_path: Path) -> bool:
        """
        Check if the path exists and if it is a directory
        """

        return dir_path.exists() and dir_path.is_dir()

    @staticmethod
    def photos_in_directory(dir_path: Path) -> list[Path]:
        """
        Returns the files in a directory in a generator
        """

        if not Photo_Manager.directory_exists(dir_path):
            return []

        return_list: list[Path] = list(
            file
            for file in dir_path.iterdir()
            if file.is_file() and file.suffix in Constants.SUPPORTED_IMAGE_EXTENSIONS
        )

        return_list.sort(key=lambda x: x.name)
        return return_list

    @staticmethod
    def photo_exists_in_archive(photo_name: str, archive_dir: Path) -> bool:
        """
        Check if the photo already exists in the archive directory
        """

        if not archive_dir.exists():
            return False

        for file in archive_dir.iterdir():
            if file.is_file() and file.name == photo_name:
                return True

        return False

    @staticmethod
    def archive_photo(current_path: Path, new_path: Path) -> None:
        """
        Move a photo found at one path to an existing folder
        """

        if not current_path.is_file():
            raise ValueError(f"'{current_path}' is not a file.")

        if new_path.exists():
            raise FileExistsError(f"Destination '{new_path}' already exists.")

        if not new_path.parent.exists():
            Path.mkdir(new_path.parent, parents=True, exist_ok=True)

        shutil.move(current_path, new_path)

    @staticmethod
    def get_coords(path: Path) -> Optional[tuple[float, float]]:
        """
        Gets coords from photo and returns them as a tuple
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            try:
                return (
                    Photo_Manager._to_decimal_coords(
                        image.gps_latitude, image.gps_latitude_ref
                    ),
                    Photo_Manager._to_decimal_coords(
                        image.gps_longitude, image.gps_longitude_ref
                    ),
                )
            except AttributeError:
                return None

    @staticmethod
    def _to_decimal_coords(coords: tuple[float, float], ref: str):
        """
        Convert coords and ref to decimal degrees format
        """

        decimal_degrees: float = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref == "S" or ref == "W":
            decimal_degrees = -decimal_degrees

        return decimal_degrees

    @staticmethod
    def get_description(path: Path) -> Optional[str]:
        """
        Get the description from the photo
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            # Return the image description if there is one
            try:
                return re.sub("\n", " ", image.image_description)
            except AttributeError:
                return None

    @staticmethod
    def get_date(path: Path) -> datetime:
        """
        Get the date and time that the photo was taken
        """

        with open(path, "rb") as src:
            image: Image = Image(src)

            # Return the image date if there is one
            try:
                return datetime.strptime(image.datetime, "%Y:%m:%d %H:%M:%S")
            except AttributeError:
                return None
