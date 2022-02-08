from __future__ import print_function
import sys


import spotipy
import spotipy.util as util
import json
import numpy as np
import pandas as pd
import os
from collections import defaultdict
from scipy.spatial.distance import cdist
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



token = util.prompt_for_user_token('ochuga','user-library-read',redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)

spotify_data = pd.read_csv('./archive(1)/tracks_features.csv')

spotify_data = spotify_data.drop(columns=['disc_number','track_number'])
song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=10, 
                                   verbose=2))],verbose=True)
X = spotify_data.select_dtypes(np.number)
number_cols = list(X.columns)
song_cluster_pipeline.fit(X)
song_cluster_labels = song_cluster_pipeline.predict(X)
spotify_data['cluster_label'] = song_cluster_labels


def find_song(name, year):
  
    """
    Takes name and release year and searches spotify api for track returning as a dataframe
    
    """
    
    song_data = defaultdict()

    #checks spotify for the song
    results = sp.search(q= 'track: {} year: {}'.format(name,
                                                       year), limit=1)
    if results['tracks']['items'] == []:
        return None
    
    results = results['tracks']['items'][0]

    #gets features for future analysis
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]
    
    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]
    #constructs for the return
    for key, value in audio_features.items():
        song_data[key] = value
    
    return pd.DataFrame(song_data)

#print(find_song("ringtone",2019))

def get_song_data(song, spotify_data):
    
    """
    Gets the song data for a specific song. 
    The song argument takes the form of a dictionary with key-value pairs for the name and release year of the song.
    checks the dataset first then looks at Spotify api if it is not found
    """
    
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name']) 
                                & (spotify_data['year'] == song['year'])].iloc[0]
        return song_data
    
    except IndexError:
        return find_song(song['name'], song['year'])




def combine_dict(dict_list):
   
    """
    Utility function for flattening a list of dictionaries.
    """
    
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def get_mean_vector(song_list, spotify_data):
  
    """
    Gets the mean vector for a list of songs.  
    """
    
    song_vectors = []
    
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)  
    
    song_matrix = np.array(list(song_vectors))
    return np.mean(song_matrix, axis=0)


def formatauth(artists):
    artists = artists.replace("'",'')
    artists = artists.replace("[",'')
    artists = artists.replace("]",'')
    return artists
    

def recommend_songs(song_list, spotify_data, n_songs=10):
  
    """
    Recommends songs based on a list of previous songs that a user has listened to.
    """
    
    metadata_cols = ['name', 'year', 'artists']
    song_dict = combine_dict(song_list)
    
    song_center = get_mean_vector(song_list, spotify_data)
    scaler = song_cluster_pipeline.steps[0][1]
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:, :n_songs][0])
    
    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[metadata_cols].to_dict(orient='records')


for song in recommend_songs([{'name': 'Come As You Are', 'year':1991},
                {'name': 'Smells Like Teen Spirit', 'year': 1991},
                {'name': 'Lithium', 'year': 1992},
                {'name': 'All Apologies', 'year': 1993},
                {'name': 'Stay Away', 'year': 1993}],  spotify_data):
                    print(f"{song['name']} by {formatauth(song['artists'])}")
                    