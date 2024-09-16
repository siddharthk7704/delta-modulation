import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
from scipy.io.wavfile import write

# Function to capture real-time audio
def record_audio(duration, sample_rate):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    return audio_data.flatten()

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
def save_as_wav(signal, file_path, sample_rate):
    # Scale signal to 16-bit PCM format
    signal_int16 = np.int16(signal * 32767)
    write(file_path, sample_rate, signal_int16)

# Function to open file dialog and save the WAV
def save_file_dialog(signal, sample_rate, title):
    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file save dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        title=title
    )

    if file_path:  # If a file path was selected
        save_as_wav(signal, file_path, sample_rate)
        print(f"File saved to {file_path}")

# Record real-time audio
duration = float(input("Enter the duration of the recording in seconds: "))  # Duration of the recording
sample_rate = 44100  # Sampling rate

# Capture audio from the microphone
original_signal = record_audio(duration, sample_rate)

# Save the original recorded audio
save_file_dialog(original_signal, sample_rate, "Save Original Audio File")

# Parameters for delta modulation
step_size = float(input("Enter the step size for the delta modulation: "))  # Step size for delta modulation

# Perform delta modulation
encoded_signal, delta_signal = delta_modulate(original_signal, step_size)

# Print the binary sequence (encoded_signal) and save it in a text file
print("\nBinary Sequence Output (first 1000 values):")
print(''.join(map(str, encoded_signal[:1000])))  # Print first 1000 bits as a string

with open("binary_output.txt", "w") as f:
    f.write(''.join(map(str, encoded_signal)))

# Calculate the quantization error (original signal - reconstructed signal)
quantization_error = original_signal[:len(delta_signal)] - delta_signal

# --- SNR Calculation ---
# Signal power (mean squared value of original signal)
signal_power = np.mean(np.square(original_signal[:len(delta_signal)]))

# Noise power (mean squared value of the quantization error)
noise_power = np.mean(np.square(quantization_error))

# SNR in dB
snr = 10 * np.log10(signal_power / noise_power)
print(f"SNR: {snr:.2f} dB")
# ------------------------

# Save the delta modulated signal as WAV
save_file_dialog(delta_signal, sample_rate, "Save Delta Modulated Audio File")

# Plot the original signal, delta modulated signal, and quantization error signal
plt.figure(figsize=(12, 12))

plt.subplot(4, 1, 1)
plt.title('Original Signal')
plt.plot(original_signal[:100000])  # Plot a portion of the signal for clarity
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
