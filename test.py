import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import find_peaks
from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_wav('C_major_scale_cut.wav')

# Convert stereo to mono
audio = audio.set_channels(1)

# Adjust the sample width to 16 bits (if needed)
audio = audio.set_sample_width(2)

# Export the processed audio
audio.export('processed_audio.wav', format='wav')

# Load the audio file
sample_rate, audio_data = wavfile.read('processed_audio.wav')

# Choose a segment of the audio for analysis
start_index = 0
end_index = 44100  # Adjust based on your requirements

# Perform FFT
fft_result = np.fft.fft(audio_data[start_index:end_index])

# Calculate the frequencies corresponding to the FFT result
frequencies = np.fft.fftfreq(len(fft_result), d=1/sample_rate)

# Plot the FFT result
plt.plot(frequencies, np.abs(fft_result))
plt.title('FFT Result')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Identify peaks in the FFT result with a threshold
threshold = 1000  # Adjust based on your specific case
peaks, _ = find_peaks(np.abs(fft_result), height=threshold)

# Convert peak indices to frequencies
identified_frequencies = frequencies[peaks]

# Print or process the identified frequencies
print('Identified Frequencies:', identified_frequencies)