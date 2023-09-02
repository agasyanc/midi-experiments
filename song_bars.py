import midi_utils as mu
import numpy as np
import pretty_midi as pm
import matplotlib.pyplot as plt


sample_file = mu.get_midi_files('midi-dataset')[61]
print(sample_file)
midi = pm.PrettyMIDI(sample_file)

bpm = midi.get_tempo_changes()[1][0]
print(bpm)
spb_bar = 60 / bpm
all_notes = mu.get_notes(midi)
print(len(all_notes))
unique_notes = mu.get_unique_notes(all_notes)
print(len(unique_notes))

mean_frequency = mu.get_mean_frequency(unique_notes, bpm)

print(100/mean_frequency)

# bars = mu.get_bars(all_notes, bpm)
# bars_vec = mu.get_bars_vectors(bars)

# output = pm.PrettyMIDI()
# inst = pm.Instrument(program=0)
# inst.notes = bars[0]
# output.instruments.append(inst)
# output.write('test.mid')