import numpy as np
import pretty_midi as pm
import midi_utils as mu
import matplotlib.pyplot as plt
import pandas as pd

songs_list = mu.get_midi_files('midi-dataset')

songs_names = []
songs_vectors = []
songs_speeds = []
songs_intenses = []
# songs_first_bar = []
songs_first_bar_vector = []

for i, path in enumerate(songs_list):
    print("Song:", i, "of", len(songs_list))
    try:
        midi_data = pm.PrettyMIDI(path)
    except:
        print("Bad file:", path)

        continue

    notes = mu.get_notes(midi_data)

    if (len(notes) > 0):
        
        songs_names.append(path)
        songs_vectors.append(mu.get_vector(notes))
        bpm = midi_data.get_tempo_changes()[1][0]
        songs_speeds.append(bpm)
        songs_intenses.append(mu.get_mean_frequency(mu.get_unique_notes(notes), bpm))
        # songs_first_bar.append(mu.get_first_bar(notes, bpm))
        songs_first_bar_vector.append(mu.get_vector(mu.get_first_quad(notes, bpm)))

# save to scv
df = pd.DataFrame(
    {'song_name': songs_names,
     'song_vector': songs_vectors,
     'song_speed': songs_speeds,
     'song_intense': songs_intenses,
     'song_first_bar_vector': songs_first_bar_vector
     }
)
df.to_csv('songs_dataset.csv')

