from . import tools


# Decodes a osu file into a object
def parse(path: str) -> str:
    headers = {}
    current_header = ""

    # Loop trough all lines of the .osu file
    for line in tools.read_file(path).split("\n"):
        # Strip the line so we wont have any additional spaces
        line = line.strip()
        # skip the line if the its is empty of if it starts with a //
        if not line or line.startswith("//"):
            continue

        # If the line starts with "[" and ends with "]" set the header into the object and skip the line
        if line.startswith('[') and line.endswith(']'):
            current_header = line.strip('[]')
            continue

        if current_header in ["General", "Difficulty"]:
            if not headers.get(current_header):
                headers[current_header] = {}

            # Function that return the key and the value
            def keyword_to_obj(str: str):
                key, value = str.split(":", 1)
                return key.strip(), tools.try_to_nr(value.strip())

            key, value = keyword_to_obj(line)

            # Assign the key and the value in the header
            headers[current_header][key] = value
            continue

        if current_header in ["TimingPoints", "HitObjects"]:
            if not headers.get(current_header):
                headers[current_header] = []

            # Variable to store the line's values in an array
            line_vals = []

            # Loop trough the values of the line
            for val in line.strip().split(","):
                # Try to convert the strings to a number
                val = tools.try_to_nr(val)
                # Append the manipulated value to the line_vals
                line_vals.append(val)

            # Append the line_vals to the current header array
            headers[current_header].append(line_vals)

    return headers
