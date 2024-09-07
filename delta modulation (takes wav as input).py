import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the WAV file
def load_wav(filename):
    sample_rate, samples = wavfile.read(filename)
    # Convert to mono if it's stereo
    if len(samples.shape) == 2:
        samples = np.mean(samples, axis=1)
    # Normalize samples to range [-1, 1]
    max_amplitude = np.max(np.abs(samples))
    normalized_samples = samples / max_amplitude
    return normalized_samples, max_amplitude, sample_rate

# Delta modulation function
def delta_modulate(signal, step_size):
    delta_signal = np.zeros(len(signal))
    encoded_signal = np.zeros(len(signal), dtype=int)
    
    # Initial values
    delta_signal[0] = signal[0]
    encoded_signal[0] = 0 if signal[0] >= 0 else 1
    
    for i in range(1, len(signal)):
        delta_signal[i] = delta_signal[i-1] + (step_size if encoded_signal[i-1] == 0 else -step_size)
        encoded_signal[i] = 0 if signal[i] >= delta_signal[i] else 1
    
    return encoded_signal, delta_signal

# Function to save the signal as WAV
def save_as_wav(signal, file_path, sample_rate, original_max_amplitude):
    # Denormalize signal to original amplitude range
    denormalized_signal = 1.67 * signal * original_max_amplitude
    # Convert to 16-bit PCM format
    signal_int16 = np.int16(denormalized_signal)
    # Write WAV file
    write(file_path, sample_rate, signal_int16)

# Function to open file dialog and save the WAV
def save_file_dialog(signal, sample_rate, original_max_amplitude):
    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file save dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        title="Save Audio File"
    )

    if file_path:  # If a file path was selected
        save_as_wav(signal, file_path, sample_rate, original_max_amplitude)
        print(f"File saved to {file_path}")

# Asks the user to load the WAV file
file_path = filedialog.askopenfilename()

# Load WAV file and convert to PCM
pcm_signal, original_max_amplitude, sample_rate = load_wav(file_path)

# Parameters for delta modulation
step_size = float(input("Enter the step size for the delta modulation: "))  # Step size for delta modulation

# Perform delta modulation
encoded_signal, delta_signal = delta_modulate(pcm_signal, step_size)

# Calculate the quantization error (original signal - reconstructed signal)
quantization_error = pcm_signal[:len(delta_signal)] - delta_signal

# Plot the original signal, delta modulated signal, and quantization error signal
plt.figure(figsize=(12, 12))

plt.subplot(4, 1, 1)
plt.title('Original Signal')
plt.plot(pcm_signal[:100000])  # Plot a portion of the signal for clarity
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 2)
plt.title('Delta Modulated Signal (Reconstructed)')
plt.step(range(len(delta_signal[:100000])), delta_signal[:100000], where='post')  # Step plot for reconstructed signal
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 3)
plt.title('Quantization Error Signal')
plt.plot(quantization_error[:100000])  # Plot a portion of the smoothed quantization error signal for clarity
plt.xlabel('Sample Index')
plt.ylabel('Quantization Error')
plt.grid(True)

plt.tight_layout()
plt.show()

# Save the delta modulated signal as WAV
save_file_dialog(delta_signal, sample_rate, original_max_amplitude)
