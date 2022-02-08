"""
asks for a genre and then will output songs based on that genre if there is a matching one
"""

from __future__ import print_function
import sys
import spotipy
import spotipy.util as util
import json

token = util.prompt_for_user_token('ochuga','user-library-read',redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)


































wantToFind = input("What genre do you like? ")

genres = sp.recommendation_genre_seeds()
for genre in genres['genres']:
   
    if genre == wantToFind:
        tracks = sp.recommendations(seed_genres=[genre])
        for track in tracks['tracks']:
            print(f"Genre {genre} returned {track['name']} {track['artists'][0]['name']}") 