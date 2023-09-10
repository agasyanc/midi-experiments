import os
import pretty_midi as pm
import numpy as np


# get all midi files from folder midi-dataset including subfolders
def get_midi_files(path):
    midi_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mid'):
                midi_files.append(os.path.join(root, file))
    return midi_files

def get_notes(midi_data):
    notes = []
    
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                notes.append(note)

    # sort notes by start time
    notes.sort(key=lambda x: x.start)                
    return notes

def get_unique_notes(notes):
    uniq = []
    for note in notes:
        is_uniq = True
        for un in uniq:
            if un.pitch == note.pitch and un.start == note.start:
                is_uniq = False
                break
        if is_uniq:
            uniq.append(note)
    return uniq

def get_mean_frequency(notes, bpm):
    durations = []
    for i, note in enumerate(notes[:-1]):
        durations.append(notes[i+1].start-note.start)
    mean_duration = np.mean(durations)
    return bpm/mean_duration

def get_vector(notes):
    vector = [0] * 12
    for note in notes:
        vector[note.pitch%12] += 1

    # normalize vector
    vector = np.array(vector, dtype=np.float32)
    if vector.max() == 0:
        return vector
    vector = vector-vector.min()
    vector = vector/vector.mean()/12
    return vector

def get_bars(notes, bpm):
    spb_bar = 60/bpm*4
    bars = []

    bar = []
    for note in notes:
        if note.start > (len(bars)+1)*spb_bar:
            bars.append(bar)
            bar = []
            bar.append(note)
            continue
        bar.append(note)
        duration = note.end-note.start
        note.start %= spb_bar
        note.end = note.start+duration

    return bars

def get_first_quad(notes, bpm):
    spb_bar = 60/bpm*4*4
    bar = []
    for note in notes:
        if note.start > spb_bar:
            break
        bar.append(note)
        duration = note.end-note.start
        note.start %= spb_bar
        note.end = note.start+duration

    return bar

def get_bars_vectors(bars):
    bars_vectors = []
    for bar in bars:
        empty_vec = [0] * 12
        for note in bar:
            empty_vec[note.pitch%12] += 1

        # normalize distribution
        for i in range(12):
            if len(bar) == 0:
                break
            empty_vec[i] /= len(bar)

        bars_vectors.append(empty_vec)
    return bars_vectors

