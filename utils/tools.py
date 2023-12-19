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

    # Return the context of the file
    return lines


# Load json file (by default load config.json)
def load_json_file(file: str = "config.json"):
    # Read and return the json file
    return json.loads(read_file(file))


# Try to make the string a number (int or float)
def try_to_nr(nr: str) -> int | float | str:
    # If its a number convert it to a number
    if nr.isdigit():
        return int(nr)
    else:
        # If its not a number try to make it a float
        # If it couldnt be converted to a float return the string back
        try:
            return float(nr)
        except Exception:
            return nr
