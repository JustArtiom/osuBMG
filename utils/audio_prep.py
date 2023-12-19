import librosa
import librosa.display
import numpy as np
from . import tools


# Generates a spectogram from a mp3 file with a hoplength of 1 ms
def create_spectrogram(file_path, n_fft=1024, n_mels=64):
    # Load the mp3 file
    y, sr = librosa.load(file_path, sr=None)
    # Make the hoplength of 1 ms
    hop_length = int(0.001 * sr)

    # Convert the mp3 file to a melspectrogram
    spectrogram = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    # Convert the spectrogram values from mel to decibels
    return librosa.power_to_db(spectrogram, ref=np.max)


# Add 0s untill you reach the target shape
def extend_to_desired_shape(spectrogram, target_shape):
    # Create a zeros numpy array shape
    padded_spectrogram = np.zeros(target_shape, dtype=spectrogram.dtype)
    # Replace the zeros with the spectrogram data
    padded_spectrogram[:spectrogram.shape[0],
                       :spectrogram.shape[1]] = spectrogram
    return padded_spectrogram


# Pad a spectrogram to a desired limit
def normalise(X, audio_limit=0):
    # Load the config.json
    config = tools.load_json_file("config.json")
    # Calculate the predicted shape
    target_shape = [config["train"]["n_mels"], audio_limit]

    # Add the audio_limit if provided or use the already defined target_shape
    target_shape[1] = audio_limit or target_shape[1]
    # Convert the target shape into a tuple
    target_shape = tuple(target_shape)

    # Pad the spectrogram to the desired shape
    return extend_to_desired_shape(X, target_shape)
