import midi_utils as mu
import numpy as np
import matplotlib.pyplot as plt
import pretty_midi as pm
import music21 as m21
import key_findind as kf


songs_list = mu.get_midi_files('midi-dataset')

print("number of songs:", len(songs_list))

songs_paths = []
songs_vectors = []
for i, path in enumerate(songs_list[:3]):
    try:
        midi_data = pm.PrettyMIDI(path)
    except:
        print("Bad file:", path)
        continue

    midi_data.write(f"{i}-original.mid")

    notes = mu.get_notes(midi_data)

    if (len(notes) > 0):
        n = []
        for note in notes:
            n.append([note.pitch, note.end-note.start])
        key = kf.find_key(n)
        maj_i = np.argmax(key[0])
        min_i = np.argmax(key[1])
        print(path, maj_i, min_i, key[0][maj_i], key[1][min_i])
        
        # if key[0][maj_i] more than key[1][min_i]
        if key[0][maj_i] > key[1][min_i]:
            # major
            curren_key = maj_i
        else:
            # minor
            curren_key = min_i+3

        for inst in midi_data.instruments:
            if not inst.is_drum:
                for note in inst.notes:
                    note.pitch -= curren_key
        
        midi_data.write(f"{i}-transposed.mid")
            
    

# print(songs_paths[2], songs_vectors[2])
# plt.bar(range(12), songs_vectors[2])
# plt.show()


# sample_song_vector = songs_vectors[34][1]

# get bar vectors
# sample_song = songs_list[0]
# print(sample_song)
# midi_data = pm.PrettyMIDI(sample_song)
# notes = mu.get_notes(midi_data)
# bpm = midi_data.get_tempo_changes()[1][0]
# bars = mu.get_bars(notes, bpm)
# print(bpm)
# bars_vectors = []
# for bar in bars:
#     empty_vec = [0] * 12
#     for note in bar:
#         empty_vec[note.pitch%12] += 1

#     # normalize distribution
#     for i in range(12):
#         empty_vec[i] /= len(bar)

#     bars_vectors.append(empty_vec)

# print(bars_vectors[0])
# print(bars[0])

