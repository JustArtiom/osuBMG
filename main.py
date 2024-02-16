import tensorflow as tf
from utils import audio_prep
import numpy as np

model = "model.h5"
model = tf.keras.models.load_model(model)

audio = "train/983911 S3RL - Bass Slut (Original Mix)/audio.mp3"

spectro = audio_prep.create_spectrogram(audio, 10, 2048, 128)
spectro = spectro[:, :10000]

predictions = model.predict(np.array([spectro]))
print(predictions)
