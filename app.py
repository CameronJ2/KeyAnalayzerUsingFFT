import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile

FILE_PATH = "C_major_scale_cut.wav"
MIN_FREQ = 0 #first note A0 is 27.50, so anything below is just noise
MAX_FREQ = 5000
NOTES = {
    "A0": 27.50, "B0" : 30.868, "C1" : 32.703, "D1" : 36.708, "E1" : 41.203, "F1" : 43.654, "G1" : 48.999, "A1" : 55.0, "B1" : 61.735, "C2" : 65.406, "D2" : 73.416, "E2" : 82.407, "F2" : 87.307, "G2" : 97.999, "A2" : 110.00, "B2" : 123.47, "C3" : 130.81, "D3" : 146.83, "E3" : 164.81, "F3" : 174.61, "G3" : 196.00, "A3" : 220.00, "B3" : 246.94, "C4" : 261.63, "D4" : 293.67, "E4" : 329.63, "F4" : 349.23, "G4" : 392.00, "A4" : 440.00, "B4" : 493.88, "C5" : 523.25, "D5" : 587.33, "E5" : 659.26, "F5" : 698.46, "G5" : 783.99, "A5" : 880.00, "B5" : 987.77, "C6" : 1046.50, "D6" : 1174.70, "E6" : 1318.50, "F6" : 1396.9, "G6" : 1568.00, "A6" : 1760.00, "B6" : 1975.00, "C7" : 2093.00, "D7" : 2349.30, "E7" : 2637.00, "F7" : 2793.00, "G7" : 3136.00, "A7" : 3520.00, "B7" : 3951.10, "C8" : 4186.00
}

AUDIO_FILE = "C_major_scale_cut.wav"
FFT_PORTIONS = 0.25 #Each FFT calculation will use .25 seconds of audio.

fs, fullData = wavfile.read(FILE_PATH)
data = fullData[:, 0] #get just the first track if the audio is multi-track

AUDIO_LENGTH = len(data) / fs #samples / sample rate = seconds


# Now that we have our data, we need to process it in chunks. Since FFT does not have a time axis, we have to make many FFT calculations at a set interval throughout the audio file to see multiple frequencies. We want the frequency with the highest amplitude for each portion

FFT_SAMPLES_PER_PORTION = FFT_PORTIONS * fs 
NUM_PORTIONS = int(np.floor(len(data) / FFT_SAMPLES_PER_PORTION))
max_frequency_over_time = []
prev_values = []
notes_played = []
prev_value = "0"
frequencies_played = []

for portion_idx in range(NUM_PORTIONS):
    start_idx = int(portion_idx * FFT_SAMPLES_PER_PORTION)
    end_idx = int(start_idx + FFT_SAMPLES_PER_PORTION)

    portion_data = data[start_idx:end_idx]
    fft_result = fft(portion_data)
    
    # Calculate the frequencies corresponding to FFT bins
    frequencies = np.fft.fftfreq(len(fft_result), 1/fs)
    
    # Filter frequencies within the specified range
    valid_freq_indices = np.where((frequencies >= MIN_FREQ) & (frequencies <= MAX_FREQ))[0]
    valid_frequencies = frequencies[valid_freq_indices]

    #Find the frequency with the highest amplitude in the valid range
    max_amplitude_index = np.argmax(np.abs(fft_result[valid_freq_indices]))
    max_amplitude_freq = frequencies[valid_freq_indices][max_amplitude_index]

    # Print or store the result for the current portion
    max_frequency_over_time.append(max_amplitude_freq)
    # Check if the last four values are the same
    if (portion_idx > 4):
        if (max_frequency_over_time[-1] == max_frequency_over_time[-2] and max_frequency_over_time[-1] > 20):
            if (prev_value != max_frequency_over_time[-1]):
                #print("4 frequencies found in sequence: {}".format(max_frequency_over_time[-1]))
                frequencies_played.append(max_frequency_over_time[-1])
            prev_value = max_frequency_over_time[-1]
    
valid_notes = []
for freq in frequencies_played:
    # Find the closest note based on the absolute difference
    closest_note = min(NOTES.items(), key=lambda x: abs(x[1] - freq))[0]
    valid_notes.append(closest_note)

for i in range(len(valid_notes) - 1):
    current_note = valid_notes[i]
    next_note = valid_notes[i + 1]

for i in range(len(valid_notes)):
    if ((i + 1) % 10 == 1 and i+1 != 11):
        print("{}st note played: {} at frequency {}".format(i + 1, valid_notes[i], frequencies_played[i]))
    elif ((i + 1) % 10 == 2 and i+1 != 12):
        print("{}nd note played: {} at frequency {}".format(i + 1, valid_notes[i], frequencies_played[i]))
    elif ((i + 1) % 10 == 3 and i+1 != 13):
        print("{}rd note played: {} at frequency {}".format(i + 1, valid_notes[i], frequencies_played[i]))
    else:
        print("{}th note played: {} at frequency {}".format(i + 1, valid_notes[i], frequencies_played[i]))