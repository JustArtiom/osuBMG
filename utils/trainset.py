from . import osu_prep, audio_prep, tools
import os


# Load Training set function
# Returns 2 arrays: parsed osu data and spectrogram of the audio
def load(path: str, log=True):
    config = tools.load_json()

    # Initialize variables for storing data
    audios = []
    maps = []

    # Loop trough the training folder
    for folder in os.listdir(path):
        # Get the dir we are currently working in
        folder_path = os.path.join(path, folder)
        # If the path is not a directory just skip it
        if not os.path.isdir(folder_path):
            continue

        # Get the mp3 file name if exists
        mp3_file = next((f for f in os.listdir(folder_path)
                         if f.lower().endswith(".mp3")), None)
        # Get the osu file name if exists
        osu_file = next((f for f in os.listdir(folder_path)
                         if f.lower().endswith(".osu")), None)

        if not mp3_file or not osu_file:
            continue

        # Get the paths of the training data
        osu_file_path = os.path.join(folder_path, osu_file)
        audio_file_path = os.path.join(folder_path, mp3_file)

        # Parse the osu file
        decoded_osu_file = osu_prep.parse(osu_file_path)

        # Filter the maps that are not in osu! mode
        if (decoded_osu_file["General"]["Mode"] != 0):
            continue

        if log:
            print(osu_file)

        maps.append(decoded_osu_file)
        audios.append(audio_prep.create_spectrogram(
            file_path=audio_file_path,
            hop_length=config["hop_length"],
            n_fft=config["n_fft"],
            n_mels=config["n_mels"]
        ))

    return audios, maps
