from utils import tools, trainset, osu_prep, audio_prep
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation
from keras.optimizers import RMSprop

# Load config.json
config = tools.load_json_file("config.json")

# Load the training set files (mp3 and .osu files)
print("\nLoading training beatmaps:\n")
audios, maps = trainset.load()

# Get the maximum audio lengths of all the files in ms
max_len = max([x.shape[1] for x in audios])

# Loop trough all the audio files and
# Pad/normalise them to the max audio len existing
for X_idx, x_mp3 in enumerate(audios):
    audios[X_idx] = audio_prep.normalise(x_mp3, max_len)

# Loop trough all maps (y axis) and convert
# and normalise them with the max audio len existing
for y_idx, y_map in enumerate(maps):
    maps[y_idx] = osu_prep.normalise(y_map, max_len=max_len)

# Convert the lists into numpy arrays
audios = np.array(audios, dtype=float)
maps = np.array(maps, dtype=str)

# Flat the array
map_tokens = maps.flatten()
# Generate a new array with unique map_tokens
map_uniq_tokens = np.unique(map_tokens)
# Generate indexes for each unique token
map_idx_tokens = {v: i for i, v in enumerate(map_uniq_tokens)}

# Get the time_span which determines how long should the short term memory last
time_span = config["train"]["time_span"]

# Convert the maps values from strings to idexes
maps = np.reshape([map_idx_tokens[i] for i in map_tokens], maps.shape)

# Get training data (concate the audio with the map)
training = np.concatenate((audios, maps), axis=1)

# Generate X and y axis
# X axis respresents a timespan with audio values and beatmap hitobjects and timingpoints
input_train = []
# Y axis represents the prediction of the next hitpoint and hitobject based on X axis
predit_train = []

# Loop trough all training sets
for train_idx, train in enumerate(training):
    # HARD TO EXPLAIN, BUT:
    # Loop trough each milisecond - time_span
    for i in range(max_len - time_span):
        if i < 0:
            continue
        # Add training set which is time_span long in ms
        input_train.append(train[:, i:i + time_span])
        # Add the next predicted hitobject and
        predit_train.append(train[-2:, i + time_span])


# Create X and Y axis
X = np.zeros((len(input_train), len(input_train[0]), time_span), dtype=float)
y = np.zeros((len(predit_train), 2, len(map_idx_tokens)), dtype=bool)

# Loop trough the predict_train
for i, train in enumerate(predit_train):
    # Loop between hitobjects and timingpoints
    for j, idx in enumerate(train):
        # Add 1 to the right value that needs to be predicted
        y[i, j, int(idx)] = 1


print(X.shape, y.shape)

# Create a model
model = Sequential()

model.add(LSTM(128, input_shape=(
    X.shape[1], time_span), return_sequences=True))
model.add(LSTM(128))
model.add(Dense(len(map_idx_tokens) * 2))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer=RMSprop(
    learning_rate=0.01), metrics=["accuracy"])
model.fit(X, y.reshape(y.shape[0], -1),
          batch_size=128, epochs=10, shuffle=True)
model.save("model.h5")
