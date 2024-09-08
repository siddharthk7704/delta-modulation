import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from scipy.io.wavfile import write
from scipy.interpolate import interp1d

# Load binary sequence from file
def load_binary_sequence(file_path):
    with open(file_path, 'r') as file:
        binary_sequence = file.read().strip()
    return np.array([int(bit) for bit in binary_sequence], dtype=int)

# Reconstruct delta-modulated signal using interpolation
def reconstruct_signal(binary_sequence, step_size, sample_rate):
    # Create a time axis for the delta-modulated steps
    t = np.arange(len(binary_sequence))
    
    # Create the delta-modulated signal (discrete steps)
    delta_signal = np.zeros(len(binary_sequence))
    delta_signal[0] = step_size if binary_sequence[0] == 0 else -step_size
    for i in range(1, len(binary_sequence)):
        delta_signal[i] = step_size if binary_sequence[i] == 0 else -step_size

    # Compute the reconstructed signal using cumulative sum of delta_signal
    reconstructed_signal = np.cumsum(delta_signal)
    
    # Interpolation to smooth the signal
    # Create a time axis for the continuous signal
    t_interp = np.linspace(0, len(binary_sequence)-1, num=len(binary_sequence)*10)
    # Interpolate the reconstructed signal
    interp_func = interp1d(t, reconstructed_signal, kind='linear', fill_value="extrapolate")
    smoothed_signal = interp_func(t_interp)

    return smoothed_signal

# Save the reconstructed signal as WAV
def save_as_wav(signal, file_path, sample_rate):
    max_amplitude = np.max(np.abs(signal))
    normalized_signal = signal / max_amplitude
    signal_int16 = np.int16(normalized_signal * 32767)
    write(file_path, sample_rate, signal_int16)

# Function to open file dialog and save the WAV
def save_file_dialog(signal, sample_rate):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
    )
    if file_path:
        save_as_wav(signal, file_path, sample_rate)
        print(f"File saved to {file_path}")

# Function to plot the reconstructed signal
def plot_signal(reconstructed_signal):
    plt.figure(figsize=(10, 6))
    plt.title('Reconstructed Signal')
    plt.plot(reconstructed_signal)
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# Main function to load binary sequence, reconstruct signal, and plot/save it
def main():
    root = tk.Tk()
    root.withdraw()

    binary_file_path = filedialog.askopenfilename(
        title="Select Binary Sequence File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not binary_file_path:
        print("No file selected.")
        return
    
    step_size = float(input("Enter the step size for the delta modulation: "))
    sample_rate = int(input("Enter the sample rate (Hz): "))
    
    # Load binary sequence from file
    binary_sequence = load_binary_sequence(binary_file_path)
    
    # Reconstruct the original signal
    reconstructed_signal = reconstruct_signal(binary_sequence, step_size, sample_rate)
    
    # Save the reconstructed signal as a WAV file
    save_file_dialog(reconstructed_signal, sample_rate)
    
    # Plot the reconstructed signal
    plot_signal(reconstructed_signal)

if __name__ == "__main__":
    main()
