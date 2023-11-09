import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks

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

    plt.plot(fft_freq, np.abs(fft_result))
    plt.title('FFT (Frequency Domain)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

    return fft_freq, np.abs(fft_result)

def identify_notes(fft_freq, fft_result):
    # Find peaks in the frequency spectrum
    peaks, _ = find_peaks(np.abs(fft_result), height=1000)  # Adjust the height threshold as needed
    
    # Mapping frequencies to musical notes
    note_freqs = {
        'C': 261.63,
        'D': 293.66,
        'E': 329.63,
        'F': 349.23,
        'G': 392.00,
        'A': 440.00,
        'B': 493.88
    }

    # Identify the closest note for each peak
    identified_notes = []
    for peak in peaks:
        closest_note = min(note_freqs, key=lambda x: abs(note_freqs[x] - fft_freq[peak]))
        identified_notes.append(closest_note)

    return peaks, identified_notes

if __name__ == "__main__":
    # Replace 'your_audio_file.wav' with the path to your WAV file
    file_path = ".\youtube_video_sample_audio_piano_c_major_scale.wav"
    
    signal, framerate = read_wav_file(file_path)
    
    # Plot the original wave graph
    plot_wave_graph(signal, framerate)
    
    # Plot the FFT graph and identify notes
    fft_freq, fft_result = plot_fft_graph(signal, framerate)
    peaks, identified_notes = identify_notes(fft_freq, fft_result)

    # Print identified notes and corresponding frequencies
    for i, note in enumerate(identified_notes):
        print(f"Peak {i+1}: {note} ({fft_freq[peaks[i]]} Hz)")