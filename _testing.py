from utils import tools, audio_prep, osu_prep
import numpy as np
# Load config.json
config = tools.load_json_file("config.json")
print("Config successfully Loaded")

# Convert a mp3 file to spectrogram
spectrogram = audio_prep.create_spectrogram(
    "__train__/1124391 LiSA - ROCK-mode/audio.mp3")
print(
    f"The spectrogram generation works. Generated with the shape {spectrogram.shape}")

# Decode a osu file to a object
osu_decoded = osu_prep.decode_file(
    "__train__/1124391 LiSA - ROCK-mode/LiSA - ROCK-mode (browiec) [Insane].osu")

timingPoints, HitObjects = osu_prep.normalise(osu_decoded, 10000)

unique_tp = np.unique(timingPoints)
unique_ho = np.unique(HitObjects)

unique_tp_index = {v: i for i,
                   v in enumerate(unique_tp)}
unique_ho_index = {v: i for i,
                   v in enumerate(unique_ho)}

input_ctx = []
next_ctx = []
