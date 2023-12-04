import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile

FILE_PATH = "C_major_scale_cut.wav"
MIN_FREQ = 0 #first note A0 is 27.50, so anything below is just noise
MAX_FREQ = 5000
NOTES = {
    "A0": [27.50, 30.867], "B0" : [30.868, 32.702], "C1" : [32.703,36.707], "D1" : [36.708, 41.202], "E1" : [41.203, 43.653], "F1" : [43.654, 48.998], "G1" : [48.999, 54.999], "A1" : [55.0, 61.734], "B1" : [61.735, 65.405], "C2" : [65.406, 73.415], "D2" : [73.416, 82.406], "E2" : [82.407, 87.306], "F2" : [87.307, 97.998], "G2" : [97.999, 109.99], "A2" : [110.00, 123.46], "B2" : [123.47, 130.80], "C3" : [130.81, 146.82], "D3" : [146.83, 164.80], "E3" : [164.81, 174.60], "F3" : [174.61, 195.99], "G3" : [196.00, 210.99], "A3" : [220.00, 246.93], "B3" : [246.94, 261.62], "C4" : [261.63, 293.66], "D4" : [293.67, 329.62], "E4" : [329.63, 249.22], "F4" : [349.23, 391.99], "G4" : [392.00, 439.99], "A4" : [440.00, 493.87], "B4" : [493.88, 523.24], "C5" : [523.25, 587.32], "D5" : [587.33, 659.25], "E5" : [659.26, 698.45], "F5" : [698.46, 783.98], "G5" : [783.99, 878.99], "A5" : [880.00, 987.76], "B5" : [987.77, 1046.49], "C6" : [1046.50, 1174.69], "D6" : [1174.70, 1318.49], "E6" : [1318.50, 1396.89], "F6" : [1396.9, 1567.99], "G6" : [1568.00, 1759.99], "A6" : [1760.00, 1975.49], "B6" : [1975.00, 2092.99], "C7" : [2093.00, 2349.29], "D7" : [2349.30, 2636.99], "E7" : [2637.00, 2792.99], "F7" : [2793.00, 3135.99], "G7" : [3136.00, 3519.99], "A7" : [3520.00, 3951.09], "B7" : [3951.10, 4185.99], "C8" : [4186.00, 5000.00]
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
        if (max_frequency_over_time[-1] == max_frequency_over_time[-2] == max_frequency_over_time[-3] == max_frequency_over_time[-4] and max_frequency_over_time[-1] > 20):
            if (prev_value != max_frequency_over_time[-1]):
                print("4 frequencies found in sequence: {}".format(max_frequency_over_time[-1]))
                frequencies_played.append(max_frequency_over_time[-1])
            prev_value = max_frequency_over_time[-1]
    
valid_notes = []
for freq in frequencies_played:
    for note, freq_range in NOTES.items():
        if freq_range[0] <= freq <= freq_range[1]:
            valid_notes.append(note)
            break
       
"""for i in range(len(valid_notes) - 1):
        current_note = valid_notes[i]
        next_note = valid_notes[i + 1]
        if current_note != next_note:
            print(current_note) """


"""     # Find the frequency with the highest amplitude in the valid range
    max_amplitude_index = np.argmax(np.abs(fft_result[valid_freq_indices]))
    max_amplitude_freq = frequencies[valid_freq_indices][max_amplitude_index]

    # Print or store the result for the current portion
    #print(f"Portion {(portion_idx + 1) * .25}: Highest Amplitude Frequency = {max_amplitude_freq} Hz")
    #max_frequency_over_time.append(max_amplitude_freq)

    #find the frequencies above the white noise threshold


    # Check if the last four values are the same
    if (portion_idx > 4):
        if (max_frequency_over_time[-1] == max_frequency_over_time[-2] == max_frequency_over_time[-3] == max_frequency_over_time[-4] and max_frequency_over_time[-1] > 20):
            if (prev_value != max_frequency_over_time[-1]):
                print("4 frequencies found in sequence: {}".format(max_frequency_over_time[-1]))
            prev_value = max_frequency_over_time[-1] """