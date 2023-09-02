import pretty_midi as pm
import midi_utils as mu
import numpy as np

files = mu.get_midi_files('midi-dataset')

bpms = []


for file in files:
    try:
        midi_data = pm.PrettyMIDI(file)
    except:
        print("Bad file:", file)
        continue

    if(len(midi_data.get_tempo_changes()[0]) == 1):
        bpms.append(midi_data.get_tempo_changes()[1][0])

bpms = np.array(bpms)

print(bpms.max(), bpms.min(), bpms.mean())
