import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
def read_wav_file(file_path):
    framerate, signal = wavfile.read(file_path)
    return signal, framerate

def plot_wave_graph(signal, framerate):
    time = np.arange(0, len(signal)) / float(framerate)
    plt.plot(time, signal)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

def plot_fft_graph(signal, framerate):
    n = len(signal)
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(n, d=1.0/framerate)
    
    # Ignore the negative frequencies
    positive_freq_mask = fft_freq > 0
    fft_freq = fft_freq[positive_freq_mask]
    fft_result = fft_result[positive_freq_mask]

    fft_result = 2.0/n * np.abs(fft_result)

    plt.plot(fft_freq, np.abs(fft_result))
    plt.title('FFT (Frequency Domain)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

if __name__ == "__main__":
    file_path = ".\\WAV_File.wav"
    
    signal, framerate = read_wav_file(file_path)
    
    # Plot the original wave graph
    plot_wave_graph(signal, framerate)
    
    # Plot the FFT graph
    plot_fft_graph(signal, framerate)