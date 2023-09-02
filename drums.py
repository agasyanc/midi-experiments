import pretty_midi as pm
import midi_utils
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import random
from music21 import note

# get all midi files from folder midi-dataset including subfolders
midi_files = midi_utils.get_midi_files('midi-dataset')

bpms = []

drum_traks = []

for midi_file in midi_files[:30]:
    try:
        midi_data = pm.PrettyMIDI(midi_file)
    except:
        print("Bad file:", midi_file)
        continue
    
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            drum_traks.append(instrument)

    bpms.append(midi_data.estimate_tempo())

print(bpms)

if (len(bpms)>0):
  print(bpms)
  normal_bpms = np.array(bpms)
  print(normal_bpms)
  normal_bpms = normal_bpms - normal_bpms.min()
  normal_bpms = normal_bpms / normal_bpms.max()

print(normal_bpms)



