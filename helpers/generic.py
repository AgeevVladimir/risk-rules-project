"""Garbage module."""
import pathlib


def fetch_all_file_names_from_project_dir(dir_name: str) -> list[str]:
    """Very self-explanotary helper."""
    return [
        one_file.stem
        for one_file in pathlib.Path(__file__).parent.parent.joinpath(dir_name).glob("*.py")
        if not one_file.stem.startswith("_")
    ]
