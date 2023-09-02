import pandas as pd
import numpy as np
# import tensorflow as tf
# import keras
# from keras import layers


# load data
songs_dataset = pd.read_csv('songs_dataset.csv', index_col=0)

# get song_vector column
songs_vectors = songs_dataset['song_vector']
print(songs_vectors.values)

# # get song_speed column
# songs_speeds = songs_dataset['song_speed']
# songs_speeds_normalized = songs_speeds / songs_speeds.max()



# song_vector_input = keras.Input(shape=(12,), name='song_vector_input')
# song_speed_input = keras.Input(shape=(1,), name='song_speed_input')
# song_intense_input = keras.Input(shape=(1,), name='song_intense_input')

# merged_input = layers.Concatenate(axis=1)([song_vector_input, song_speed_input, song_intense_input])

# dense_layer = layers.Dense(128, activation='relu', name='dense_layer')(merged_input)

# fisrt_quad_vector_output = layers.Dense(12, activation='relu', name='fisrt_quad_vector_output')(dense_layer)

# first_bar_generator_model = keras.Model(inputs=[song_vector_input, song_speed_input, song_intense_input], outputs=fisrt_quad_vector_output)

# first_bar_generator_model.summary()


# first_bar_generator_model.compile(optimizer='adam', loss='mse')


# first_bar_generator_model.fit(x=[songs_vectors, songs_speeds_normalized, songs_intenses_normalized], y=songs_first_bar_vector, epochs=10)

# first_bar_generator_model.save( 'models/first_bar_generator_model')