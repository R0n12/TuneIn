from __future__ import print_function
#from ossaudiodev import SNDCTL_COPR_SENDMSG
import sys
import spotipy
import spotipy.util as util
import json

token = util.prompt_for_user_token('ochuga','user-library-read',redirect_uri='http://localhost:8080')

sp = spotipy.Spotify(auth=token)

def sfind(wantToFind):
    
    songs = []
    genres = sp.recommendation_genre_seeds()
    for genre in genres['genres']:
   
        if genre == wantToFind:
         tracks = sp.recommendations(seed_genres=[genre])
         for track in tracks['tracks']:
              songs.append(f"{track['name']} by {track['artists'][0]['name']}   ")
    return songs