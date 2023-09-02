import numpy as np
import pretty_midi as pm
import midi_utils as mu
import matplotlib.pyplot as plt
import random
from music21 import note


midi_files = mu.get_midi_files('midi-dataset')

# sample_file = midi_files[2]
sample_file = "midi-dataset/a-ha/Take On Me.2.mid"
print(sample_file)

print(sample_file)

# read midi file
midi_file = pm.PrettyMIDI(sample_file)

bpm = midi_file.estimate_tempo()

print(bpm)

# get all notes exept drums
notes = []

for instrument in midi_file.instruments:
    if not instrument.is_drum:
        notes.extend(instrument.notes)

sorted_notes = sorted(notes, key=lambda note: note.start)

# seconds per beat
spb = 60.0 / bpm

# seconds per bar
spb_bar = spb * 4

bars = []
bar = []
for note in sorted_notes:
    if note.start > len(bars)*spb_bar:
        if len(bar) > 0:
          bars.append(bar)
        bar = []
        bar.append(note)
    bar.append(note)


bar_vec = []
for bar in bars:
    vec = []
    for note in bar:
        # normalize from 0 to 11
        normal_pitch = note.pitch % 12
        vec.append(normal_pitch)

    # make empty vector of length 12
    empty_vec = np.zeros(12)

    # count distribution of pitches
    for pitch in vec:
        empty_vec[pitch] += 1

    # normalize distribution
    for i in range(12):
        empty_vec[i] /= len(vec)

    
    bar_vec.append(empty_vec)


print(bar_vec[56])
print(bars[56])

for bar in bars:
    for note in bar:
        # normalize start to bar
        note.start %= spb_bar
        note.end %= spb_bar

        # print(note.start, note.end, note.pitch)

print(bars[56])

