# expense_tracker/view/popup/popup_utils.py

from pathlib import Path

from expense_tracker.model.photo_manager import Photo_Manager


class Popup_Utils:
    @staticmethod
    def _file_exists(input: str) -> bool:
        path: Path = Popup_Utils._get_path(input)
        return path.exists() and path.is_file()

    @staticmethod
    def _file_is_csv(input: str) -> bool:
        path: Path = Popup_Utils._get_path(input)
        return path.suffix == ".csv"

    @staticmethod
    def _directory_exists(input: str) -> bool:
        path: Path = Popup_Utils._get_path(input)
        return Photo_Manager.directory_exists(path)

    @staticmethod
    def _photos_in_directory(input: str) -> bool:
        path: Path = Popup_Utils._get_path(input)
        return len(Photo_Manager.photos_in_directory(path)) > 0

    @staticmethod
    def _get_path(input: str) -> Path:
        return Path(input.replace("'", ""))
