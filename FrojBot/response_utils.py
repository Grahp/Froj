import os
import json


def get_file_path() -> str:
    "Returns the dir this script is being executed in."
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # __file__ is not set in interactive environments, falls back to cwd.
        return os.getcwd()


base_dir = get_file_path()


def load_json(file_path: str) -> dict:
    "Loads JSON from a given file path, or None if the file does not exist."
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

