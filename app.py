import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile

FILE_PATH = "C_major_scale_cut.wav"
MIN_FREQ = 10
MAX_FREQ = 1000
NOTES = {
    "A0": [27.50, 30.867], "B0" : [30.868, 32.702], "C1" : [32.703,36.707], "D1" : [36.708, 41.202], "E1" : [41.203, 43.653], "F1" : [43.654, 48.998], "G1" : [48.999, 54.999], "A1" : [55.0, 61.734], "B1" : [61.735, 65.405], "C2" : [65.406, 73.415], "D2" : [73.416, 82.406], "E2" : [82.407, 87.306], "F2" : [87.307, 97.998], "G2" : [97.999], "A2" : [], "B2" : [], "C3" : [], "D3" : [], "E3" : [], "F3" : [], "G3" : [], "A3" : [], "B3" : [], "C4" : [], "D4" : [], "E4" : [], "F4" : [], "G4" : [], "A4" : [], "B4" : [], "C5" : [], "D5" : [], "E5" : [], "F5" : [], "G5" : [], "A5" : [], "B5" : [], "C6" : [], "D6" : [], "E6" : [], "F6" : [], "G6" : [], "A6" : [], "B6" : [], "C7" : [], "D7" : [], "E7" : [], "F7" : [], "G7" : [], "A7" : [], "B7" : [], "C8" : []
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

for portion_idx in range(NUM_PORTIONS):
    start_idx = int(portion_idx * FFT_SAMPLES_PER_PORTION)
    end_idx = int(start_idx + FFT_SAMPLES_PER_PORTION)

    portion_data = data[start_idx:end_idx]
    fft_result = fft(portion_data)
    
    # Calculate the frequencies corresponding to FFT bins
    frequencies = np.fft.fftfreq(len(fft_result), 1/fs)
    
    # Filter frequencies within the specified range
    valid_freq_indices = np.where((frequencies >= MIN_FREQ) & (frequencies <= MAX_FREQ))[0]
    
    # Find the frequency with the highest amplitude in the valid range
    max_amplitude_index = np.argmax(np.abs(fft_result[valid_freq_indices]))
    max_amplitude_freq = frequencies[valid_freq_indices][max_amplitude_index]

    # Print or store the result for the current portion
    #print(f"Portion {(portion_idx + 1) * .25}: Highest Amplitude Frequency = {max_amplitude_freq} Hz")
    max_frequency_over_time.append(max_amplitude_freq)


    # Check if the last four values are the same
    if (portion_idx > 4):
        if (max_frequency_over_time[-1] == max_frequency_over_time[-2] == max_frequency_over_time[-3] == max_frequency_over_time[-4] and max_frequency_over_time[-1] > 20):
            if (prev_value != max_frequency_over_time[-1]):
                print("4 frequencies found in sequence: {}".format(max_frequency_over_time[-1]))
            prev_value = max_frequency_over_time[-1]

            """ # Find the note corresponding to the detected frequency
            detected_frequency = max_frequency_over_time[-1]
            detected_note = None

            for note, freq_range in NOTES.items():
                if freq_range[0] <= detected_frequency <= freq_range[1]:
                    detected_note = note
                    break

            if detected_note:
                notes_played.append(detected_note)
                print("Note played: {}".format(detected_note)) """



#https://newt.phys.unsw.edu.au/jw/notes.html
#https://newt.phys.unsw.edu.au/music/note/


""" 
Encountered troubles:
    Time Domain vs Frequency Domain and "frequency bins"
    multi-channel
    

Concerns:
    try and convert to video?
    
"""