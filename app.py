import matplotlib.pyplot as plt
from scipy.fftpack import fft
import numpy as np
from scipy.io import wavfile

FILE_PATH = "c_major_scale_cut.wav"
MIN_FREQ = 0
MAX_FREQ = 8000
NOTES = {
    "C0": 16.35, "C#0/Db0": 17.32, "D0": 18.35, "D#0/Eb0": 19.45, "E0": 20.60, "F0": 21.83, "F#0/Gb0": 23.12,
    "G0": 24.50, "G#0/Ab0": 25.96, "A0": 27.50, "A#0/Bb0": 29.14, "B0": 30.87, "C1": 32.70, "C#1/Db1": 34.65,
    "D1": 36.71, "D#1/Eb1": 38.89, "E1": 41.20, "F1": 43.65, "F#1/Gb1": 46.25, "G1": 49.00, "G#1/Ab1": 51.91,
    "A1": 55.00, "A#1/Bb1": 58.27, "B1": 61.74, "C2": 65.41, "C#2/Db2": 69.30, "D2": 73.42, "D#2/Eb2": 77.78,
    "E2": 82.41, "F2": 87.31, "F#2/Gb2": 92.50, "G2": 98.00, "G#2/Ab2": 103.83, "A2": 110.00, "A#2/Bb2": 116.54,
    "B2": 123.47, "C3": 130.81, "C#3/Db3": 138.59, "D3": 146.83, "D#3/Eb3": 155.56, "E3": 164.81, "F3": 174.61,
    "F#3/Gb3": 185.00, "G3": 196.00, "G#3/Ab3": 207.65, "A3": 220.00, "A#3/Bb3": 233.08, "B3": 246.94, "C4": 261.63,
    "C#4/Db4": 277.18, "D4": 293.66, "D#4/Eb4": 311.13, "E4": 329.63, "F4": 349.23, "F#4/Gb4": 369.99, "G4": 392.00,
    "G#4/Ab4": 415.30, "A4": 440.00, "A#4/Bb4": 466.16, "B4": 493.88, "C5": 523.25, "C#5/Db5": 554.37, "D5": 587.33,
    "D#5/Eb5": 622.25, "E5": 659.25, "F5": 698.46, "F#5/Gb5": 739.99, "G5": 783.99, "G#5/Ab5": 830.61, "A5": 880.00,
    "A#5/Bb5": 932.33, "B5": 987.77, "C6": 1046.50, "C#6/Db6": 1108.73, "D6": 1174.66, "D#6/Eb6": 1244.51, "E6": 1318.51,
    "F6": 1396.91, "F#6/Gb6": 1479.98, "G6": 1567.98, "G#6/Ab6": 1661.22, "A6": 1760.00, "A#6/Bb6": 1864.66, "B6": 1975.53,
    "C7": 2093.00, "C#7/Db7": 2217.46, "D7": 2349.32, "D#7/Eb7": 2489.02, "E7": 2637.02, "F7": 2793.83, "F#7/Gb7": 2959.96,
    "G7": 3135.96, "G#7/Ab7": 3322.44, "A7": 3520.00, "A#7/Bb7": 3729.31, "B7": 3951.07, "C8": 4186.01, "C#8/Db8": 4434.92,
    "D8": 4698.63, "D#8/Eb8": 4978.03, "E8": 5274.04, "F8": 5587.65, "F#8/Gb8": 5919.91, "G8": 6271.93, "G#8/Ab8": 6644.88,
    "A8": 7040.00, "A#8/Bb8": 7458.62, "B8": 7902.13
}


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

    #Find the frequency with the highest amplitude in the valid range
    max_amplitude_index = np.argmax(np.abs(fft_result[valid_freq_indices]))
    max_amplitude_freq = frequencies[valid_freq_indices][max_amplitude_index]


    # Print or store the result for the current portion
    max_frequency_over_time.append(max_amplitude_freq)
    


    # Check if the last four values are the same
    if (portion_idx > 4):
        if (max_frequency_over_time[-1] == max_frequency_over_time[-2] == max_frequency_over_time[-3] == max_frequency_over_time[-4] and max_frequency_over_time[-1] > 20):
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