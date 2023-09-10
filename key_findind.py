import numpy as np
import pretty_midi as pm



def transpose_pm(midi:pm.PrettyMIDI) -> pm.PrettyMIDI:
  notes = []

  for instrument in midi.instruments:
    if instrument.is_drum:
      continue
    for note in instrument.notes:
      notes.append(note)

  notes = list( map( lambda note: [note.pitch, note.end - note.start],  notes))

  keys = find_key(notes)

  maj_i = np.argmax(keys[0])
  min_i =np.argmax(keys[1])
  print(maj_i, keys[0][maj_i], min_i,  keys[1][min_i])

  if keys[0][maj_i] > keys[1][min_i]:
      # major
      current_key = maj_i
  else:
      # minor
      current_key = min_i+3

  print(current_key)

  for inst in midi.instruments:
      if not inst.is_drum:
          for note in inst.notes:
              print("before", note.pitch)
              note.pitch -= current_key
              print("after", note.pitch)
    
  return midi


def find_key(notes):
  pitches = np.array([note[0] for note in notes])
  durations = np.array([note[1] for note in notes])
  pitches = pitches % 12
  [[12,45],[0.23, 1.3]]

  pitch_durations = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}

  for i, pitch in enumerate(pitches):
    pitch_durations[pitch] += durations[i]

  # print(pitch_durations)
  pitch_durations = list(pitch_durations.values())

  major_profile = [6.35, 2.32, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
  minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

  # calculate relarions
  pitch_durations_mean = np.mean(pitch_durations)

  maj_correlations = []
  min_correlations = []
  # major corelation
  for i in range(12):

    major_profile_mean = np.mean(major_profile) 
    minor_profile_mean = np.mean(minor_profile)

    maj_t_sum = 0.0
    min_t_sum = 0.0
    maj_a_sum = 0.0
    min_a_sum = 0.0
    maj_b_sum = 0.0
    min_b_sum = 0.0
    for i in range(12):
      maj_t_sum += (pitch_durations[i]-pitch_durations_mean)*(major_profile[i]-major_profile_mean)
      min_t_sum += (pitch_durations[i]-pitch_durations_mean)*(minor_profile[i]-minor_profile_mean)

      maj_a_sum += (pitch_durations[i]-pitch_durations_mean)**2
      min_a_sum += (pitch_durations[i]-pitch_durations_mean)**2

      maj_b_sum += (major_profile[i]-major_profile_mean)**2
      min_b_sum += (minor_profile[i]-minor_profile_mean)**2

    maj_correlations.append(maj_t_sum/np.sqrt(maj_a_sum*maj_b_sum))
    min_correlations.append(min_t_sum/np.sqrt(min_a_sum*min_b_sum))

    # shift profile
    major_profile = np.roll(major_profile, 1)
    minor_profile = np.roll(minor_profile, 1)

  return [maj_correlations, min_correlations]
  
def find_key_str(notes):
  keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
  maj_correlations, min_correlations = find_key(notes)
  if max(maj_correlations) > max(min_correlations):
    key_name = keys[np.argmax(maj_correlations)]
    return f"{key_name} major"
  else:
    key_name = keys[np.argmax(min_correlations)]
    return f"{key_name} minor"

