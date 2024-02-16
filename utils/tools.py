import os
import json


# File to string
def read_file(path: str) -> str:
    # Check if file exists
    if not os.path.isfile(path):
        raise Exception("File not found")

    # Load the file and define the context
    with open(path, 'r', encoding='utf-8') as stream:
        lines = stream.read()

    return lines


# Load json file (by default load config.json)
def load_json(file: str = "config.json"):
    return json.loads(read_file(file))


# Try to make the string a number (int or float)
def try_to_nr(nr: str) -> int | float | str:
    if nr.isdigit():
        return int(nr)
    else:
        try:
            return float(nr)
        except Exception:
            return nr
