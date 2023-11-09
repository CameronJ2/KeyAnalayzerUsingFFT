import matplotlib.pyplot as plt #for the graphical output.
import wave #for processing .wav audio files. We will be using .wav files because they're the highest quality available with minimal compression.
import numpy #needed for the FFT algorithm.
import os #only necessary for getting your current working directory.

#First we need to set up the wav file we're going to use. I'm going to start with the sample file from the youtube video

def read_wav_file(file_path):
    with wave.open(file_path, 'rb') as wf:
        framerate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
        signal = numpy.frombuffer(frames, dtype=numpy.int16)
    return signal, framerate

def plot_wave_graph(signal, framerate):
    time = numpy.arange(0, len(signal)) / float(framerate)
    plt.plot(time, signal)
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

def plot_fft_graph(signal, framerate):
    n = len(signal)
    fft_result = numpy.fft.fft(signal)
    fft_freq = numpy.fft.fftfreq(n, d=1.0/framerate)
    
    # Ignore the negative frequencies
    positive_freq_mask = fft_freq > 0
    fft_freq = fft_freq[positive_freq_mask]
    fft_result = fft_result[positive_freq_mask]

    plt.plot(fft_freq, numpy.abs(fft_result))
    plt.title('FFT (Frequency Domain)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

if __name__ == "__main__": #Not necessary, but good practice.

    # Replace 'your_audio_file.wav' with the path to your WAV file
    file_path = r".\youtube_video_sample_audio_piano_c_major_scale.wav"
    
    signal, framerate = read_wav_file(file_path)
    
    # Plot the original wave graph
    plot_wave_graph(signal, framerate)
    
    # Plot the FFT graph
    plot_fft_graph(signal, framerate)