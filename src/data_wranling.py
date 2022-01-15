#!/usr/bin/env python3

'''
This modole contains functions for getting data from Spotify API

'''



########################################################################
## Import librarys

import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import config



########################################################################
## Set connections with API

def get_spotify_connection() -> spotipy.client.Spotify:
    """
    Returns a spotipy client connection based on the keys stored in the file "config.py"
    
    Output:
      - sp: spotipy client connection
    """
    
    cid = config.acces_credentials.get('client_id')
    secret = config.acces_credentials.get('secret_id')
    
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)
    
    return sp

## get playist features to a pandas dataframe

def playlist_features(playlist_id: str, sp=get_spotify_connection()):
    '''
    Create a pandas dataframe with the features of the trakcs extracted from a playlist.
    
    Input:
        -playlist_id: string with the playlist id.
        -sp: spotipy client
        
    Output:
        -pandas dataframe with the features of the tracks in the playlist.
    '''
    
    # get playlist total len
    playlist_len = sp.playlist_tracks(playlist_id=playlist_id, limit=1)['total']

    # define empty lists for the features
    track_id = []
    track_name = []
    duration_ms = []
    explicit = []
    track_popularity = []

    artist_name = []
    artist_id = []

    album_name = []
    album_id = []
    album_type = []
    release_date = []

    acousticness = []
    danceability = []
    energy = []
    instrumentalness = []
    key = []
    liveness = []
    loudness = []
    mode = []
    speechiness = []
    tempo = []
    time_signature = []
    valence = []

    artist_popularity = []
    artist_genres = []
    artist_followers = []


    # get features in batches
    for i in range(0,playlist_len,50):
        playlist = sp.playlist_tracks(playlist_id=playlist_id, limit=50, offset=i)

        for t in playlist['items']:
            # tracks characteristics
            track_id.append(t['track']['id'])
            track_name.append(t['track']['name'])
            duration_ms.append(t['track']['duration_ms'])
            explicit.append(t['track']['explicit'])
            track_popularity.append(t['track']['popularity'])

            # artist characteristics
            artist_name.append(t['track']['artists'][0]['name'])
            artist_id.append(t['track']['artists'][0]['id'])

            # album characteristics
            album_name.append(t['track']['album']['name'])
            album_id.append(t['track']['album']['id'])
            album_type.append(t['track']['album']['type'])
            release_date.append(t['track']['album']['release_date'])

            # get tracks features
            batch_track_features = sp.audio_features(tracks=track_id[i:])

            # get artists fetures
            batch_artist_features = sp.artists(artist_id[i:])['artists']

        # add tracks' feature for the current batch    
        acousticness = acousticness + [feature['acousticness'] for feature in batch_track_features]
        danceability = danceability + [feature['danceability'] for feature in batch_track_features]
        energy = energy + [feature['energy'] for feature in batch_track_features]
        instrumentalness = instrumentalness + [feature['instrumentalness'] for feature in batch_track_features]
        key = key + [feature['key'] for feature in batch_track_features]
        liveness = liveness + [feature['liveness'] for feature in batch_track_features]
        loudness = loudness + [feature['loudness'] for feature in batch_track_features]
        mode = mode + [feature['mode'] for feature in batch_track_features]
        speechiness = speechiness + [feature['speechiness'] for feature in batch_track_features]
        tempo = tempo + [feature['tempo'] for feature in batch_track_features]
        time_signature = time_signature + [feature['time_signature'] for feature in batch_track_features]
        valence = valence + [feature['valence'] for feature in batch_track_features]

        # add artists' feature for the current batch
        artist_popularity = artist_popularity + [feature['popularity'] for feature in batch_artist_features]
        artist_genres = artist_genres + [feature['genres'] for feature in batch_artist_features]
        artist_followers = artist_followers + [feature['followers']['total'] for feature in batch_artist_features]
        
    # convert to pandas dataframe
    df_playlist = pd.DataFrame({
        'track_id': track_id,
        'track_name': track_name,
        'duration_ms': duration_ms,
        'explicit': explicit,
        'track_popularity': track_popularity,
        'acousticness': acousticness,
        'danceability': danceability,
        'energy': energy,
        'instrumentalness': instrumentalness,
        'key': key,
        'liveness': liveness,
        'loudness': loudness,
        'mode': mode,
        'speechiness': speechiness,
        'tempo': tempo,
        'time_signature': time_signature,
        'valence': valence,
        'artist_name': artist_name,
        'artist_id': artist_id,
        'artist_popularity': artist_popularity,
        'artist_genres': artist_genres,
        'artist_followers': artist_followers,
        'album_name': album_name,
        'album_id': album_id,
        'album_type': album_type,
        'release_date': release_date
    })
    
    return df_playlist


########################################################################

def main():
	pass
	
if __name__ == "__main__":
	main()