import requests
import pandas as pd
import playlists


def load_secrets(fname='secrets.txt'):
    secrets = []
    with open(fname) as f:
        for line in f.readlines():
            secrets.append(line.strip())
    return tuple(secrets)


def auth_spotify(client_id, client_secret):
    URl = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(URl, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,

    })

    auth_response = auth_response.json()
    access_token = auth_response['access_token']
    return access_token


def get_artist(artist_id, access_token):
    header = {'Authorization': f"Bearer {access_token}"}
    URl = f'https://api.spotify.com/v1/artists/{artist_id}'

    artist_feature = requests.get(URl, headers=header)
    artist_feature = artist_feature.json()
    return artist_feature


def get_profile(access_token):
    header = {'Authorization': f"Bearer {access_token}"}
    URl = 'https://api.spotify.com/v1/me'

    profile_feature = requests.get(URl, headers=header)
    return profile_feature.json()


if __name__ == "__main__":
    # Request access token
    secrets = load_secrets()
    access_token = auth_spotify(*secrets)
    print("token", access_token)

    # # Get some artist data
    # artist_id = "1eDIWVJt7ZWKsrXw5WVNsN?si=7b4c07a5bf5146ff"
    # artist_response = get_artist(artist_id, access_token)

    # Get playlist data
    # playlist_id = "5XPDIbCZaBGHnlLfNqhQYk?si=12b0ebee4a674d39"
    playlist_id = "4jw7qBh5XcL7sT2AKgKg8R?si=12ed34e093cf4f78"
    playlist_response = playlists.get_playlist(playlist_id, access_token)

    playlist_df = playlists.playlist_to_df(playlist_response)
    # playlist_df.to_csv("my_playlist.csv", index=False)



