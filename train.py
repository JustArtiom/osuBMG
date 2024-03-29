from keras.callbacks import ModelCheckpoint, EarlyStopping
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Reshape, Flatten, LSTM, Dense, TimeDistributed, BatchNormalization, Dropout
import numpy as np
from utils import tools, trainset, audio_prep

config = tools.load_json()

print("")
print(f"Welcome to BMG!osu")
print(f"Training script version:     {config['version']}")
print("")
print(f"Training directory set to:   {config['training_path']}")
print(f"Output directory set to:     {config['output_path']}")
print("")

# Loading the spectrograms and parsed osu files
print("Loading Training set...")
print("")
audios, maps = trainset.load(config['training_path'], log=True)
print("")

# Pad the spectograms to get them to the same size
audios = audio_prep.pad_spectrograms(audios)

# Convert the osu files into an array of timing points of when a beat should be played
maps = [[round(hit_object[2] / config["hop_length"]) for hit_object in osu_map["HitObjects"]]
        for osu_map in maps]

# Convert the array of timing points into a array of
# 1 and 0 when the beat should be played for each hop_length
max_len = audios.shape[2]
tmp_maps = []
for osu_map in maps:
    zero_map = np.zeros((max_len), dtype=int)
    for tp in osu_map:
        zero_map[tp] = 1
    tmp_maps.append(zero_map)
maps = np.array(tmp_maps)

# Apply the maximum in case it exceeds the limit in the configuration
max_value = int((config["max_len"] or max_len) / config["hop_length"])
audios = audios[:, :, :max_value]
audios = audios.transpose(0, 2, 1)
maps = maps[:, :max_value]

print(f"Audio files with a shape of: {audios.shape}")
print(f"Osu maps with a shape of: {maps.shape}")
