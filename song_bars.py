import midi_utils as mu
import key_findind as kf
import numpy as np
import pretty_midi as pm
import tensorflow as tf
import keras
from keras import layers

# get all file paths
sample_files = mu.get_midi_files('midi-dataset')

all_bars = []
all_vectors = []
all_notes = []

# load all midi files
for i, sample_file in enumerate(sample_files[:200]):
    try:
      midi = pm.PrettyMIDI(sample_file)
      print(i, sample_file)
    except:
      print("Bad file:", sample_file)
      continue
    
    # if tempo changes more than 1, then skip
    if len(midi.get_tempo_changes()[0]) > 1:
      continue
    
    # get bpm
    bpm = midi.get_tempo_changes()[1][0]
    # get all notes
    all_midi_notes = mu.get_notes(midi)
    # remove duplicate notes
    unique_notes = mu.get_unique_notes(all_midi_notes)

    # prepare notes for key finding
    n = []
    for note in unique_notes:
      n.append([note.pitch, note.end - note.start])

    # find key of the song
    key = kf.find_key(n)
    maj_i = np.argmax(key[0])
    min_i = np.argmax(key[1])

    # find current key
    if key[0][maj_i] > key[1][min_i]:
        # major
        current_key = maj_i
    else:
        # minor
        current_key = min_i+3
    # transpose unique notes
    for note in unique_notes:
        note.pitch -= current_key
    bars = mu.get_bars(unique_notes, bpm)
    # add bars to bars list
    all_bars.append(bars)

    # get bar vectors
    for bar in bars:
      all_vectors.append(mu.get_vector(bar))
      notes = [[]]*12
      for i in range(12):
          notes[i] = [0]*128
          for k in range(128):
              notes[i][note.pitch] = 1

      all_notes.append(notes)

all_vectors = np.array(all_vectors, dtype=np.float32)
all_notes = np.array(all_notes, dtype=np.float32)
all_notes = np.reshape(all_notes, (all_notes.shape[0], 12*128))

print("vector", all_vectors.shape, all_vectors.dtype, all_vectors[0], all_vectors.max(), all_vectors.min())
print("notes", all_notes.shape, all_notes.dtype, all_notes[0], all_notes.max(), all_notes.min())


# first bar to notes model
input_layer = layers.Input(shape=(12))
x = layers.Dense(1024, activation='relu')(input_layer)
y = layers.Dense(128, activation='relu')(x)
output_layer = layers.Dense(12*128)(y)

model = keras.Model(inputs=input_layer, outputs=output_layer)

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
model.fit(all_vectors, all_notes, epochs=10, batch_size=128, validation_split=0.2)

model.save('first_bar_to_notes_model')

x = np.array([[0,0,.2,0,0.4,0,0,1,0,0.3,0,.1]])

pred = model.predict(x)
pred = np.reshape(pred, (12, 128))


# create new midi

new_midi = pm.PrettyMIDI()
track = pm.Instrument(program=0)
new_midi.instruments.append(track)

for i, p in enumerate(pred):
    pitch = np.argmax(p)
    duration = 0.5
    velocity = 100
    note = pm.Note(velocity=velocity, pitch=pitch, start=i*duration, end=i*duration+duration)

    track.notes.append(note)

new_midi.write('test.mid')
