import midi_utils as mu
import numpy as np
import matplotlib.pyplot as plt
import pretty_midi as pm

songs_list = mu.get_midi_files('midi-dataset')

print(len(songs_list))

songs_vectors = []
for path in songs_list[:3]:
    try:
        midi_data = pm.PrettyMIDI(path)
    except:
        print("Bad file:", path)
        
        continue
    
    notes = mu.get_notes(midi_data)

    if (len(notes) > 0):
        # get unique pitches
        vector = mu.get_vector(notes)

        songs_vectors.append([path, vector])
        # print(songs_vectors)

# sample_song_vector = songs_vectors[34][1]

# get bar vectors
sample_song = songs_list[0]
print(sample_song)
midi_data = pm.PrettyMIDI(sample_song)
notes = mu.get_notes(midi_data)
bpm = midi_data.get_tempo_changes()[1][0]
bars = mu.get_bars(notes, bpm)
print(bpm)
bars_vectors = []
for bar in bars:
    empty_vec = [0] * 12
    for note in bar:
        empty_vec[note.pitch%12] += 1

    # normalize distribution
    for i in range(12):
        empty_vec[i] /= len(bar)

    bars_vectors.append(empty_vec)

print(bars_vectors[0])
print(bars[0])

