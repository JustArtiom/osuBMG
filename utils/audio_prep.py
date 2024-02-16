import librosa
import librosa.display
import numpy as np


# Generates a spectogram from a audio file
def create_spectrogram(file_path, hop_length, n_fft=2048, n_mels=128):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)
    # Make the hoplength of 1 ms
    hop_length = int(hop_length / 1000 * sr)

    # Convert the mp3 file to a melspectrogram
    spectrogram = librosa.feature.melspectrogram(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    # Convert the spectrogram values from mel to decibels
    spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    return (spectrogram - spectrogram.min()) / (spectrogram.max() - spectrogram.min())


# Function to pad a list of spectrograms to the same size
def pad_spectrograms(spectrograms, t=0):
    # Determine the maximum dimensions among all spectrograms
    max_time_frames = t or max(spec.shape[1] for spec in spectrograms)
    max_frequency_bins = max(spec.shape[0] for spec in spectrograms)

    # Pad each spectrogram to match the maximum dimensions
    padded_spectrograms = []
    for spec in spectrograms:
        pad_time_frames = max_time_frames - spec.shape[1]
        pad_frequency_bins = max_frequency_bins - spec.shape[0]
        # Pad the spectrogram along the time and frequency dimensions
        padded_spec = np.pad(spec, ((0, pad_frequency_bins),
                             (0, pad_time_frames)), mode='constant', constant_values=0)
        padded_spectrograms.append(padded_spec)

    return np.array(padded_spectrograms)
