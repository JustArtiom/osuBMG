from . import tools, osu_prep, audio_prep
import os


# Load Training set function
# Returns 2 arrays with an already converted mp3 file to a spectrogram
# and decoded osu file
def load(log=True):
    # Load config.json
    config = tools.load_json_file("config.json")

    # Variables to store the X and y axis for training
    X = []
    y = []

    # Loop trough the folders
    for folder in os.listdir(config["train"]["path"]):
        # Get the folder path in the current folder that we are in
        folder_path = os.path.join(config["train"]["path"], folder)

        # If the path is not a dir (but is a file) just skip it
        if not os.path.isdir(folder_path):
            continue

        # Load the mp3 file found (if found)
        mp3_file = next((f for f in os.listdir(folder_path)
                         if f.lower().endswith(".mp3")), None)
        # Load the osu file found (if foundc)
        osu_file = next((f for f in os.listdir(folder_path)
                         if f.lower().endswith(".osu")), None)

        # If there is no osu file or mp3 file just skip
        if not mp3_file or not osu_file:
            continue

        # Decode the osu file
        decoded_osu_file = osu_prep.decode_file(
            os.path.join(folder_path, osu_file))

        # Allow only osu game mode files
        if (decoded_osu_file["General"]["Mode"] != 0):  # Osu mode only!
            continue

        # Log the current folder we are manipulating
        if log:
            print(osu_file)

        # Convert and append the mp3 file to the X axis as a spectrogram in db
        X.append(audio_prep.create_spectrogram(
            os.path.join(folder_path, mp3_file),
            config["train"]["n_fft"],
            config["train"]["n_mels"]))
        # Append to the decoded y axis to the y axis
        y.append(decoded_osu_file)

    # Return the training axes
    return X, y
