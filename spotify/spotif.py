from http import client
import json
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

# SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
# API_VERSION = "v1"
# SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# client keys
CLIENT = json.load(open('config.json', 'r+'))
CLIENT_ID = CLIENT['c_id']
CLIENT_SECRET = CLIENT['c_secret']


CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET))

results = sp.search(q='Eminem', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['artists'][0]['name'], " – ", track['name'])

# GET_ARTIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'artists')
# def get_artist(artist_id):
#     url = "{}/{id}".format(GET_ARTIST_ENDPOINT, id=artist_id)
#     resp = requests.get(url)
#     return resp.json()