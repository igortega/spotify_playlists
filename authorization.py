import requests
import pandas as pd


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


def get_playlist(playlist_id, access_token):
    header = {'Authorization': f"Bearer {access_token}"}
    URl = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    profile_feature = requests.get(URl, headers=header)
    return profile_feature.json()


def playlist_to_df(playlist_json):
    tracks = playlist_json["tracks"]["items"]
    n_tracks = len(tracks)
    # print(n_tracks, tracks)
    playlist_dict = {"name": [],
                     "artist": [],
                     "album": [],
                     "id": [],
                     "popularity": [],
                     "duration": [],
                     }

    for i in range(n_tracks):
        track = tracks[i]["track"]
        playlist_dict["name"].append(track["name"])
        playlist_dict["artist"].append(track["artists"][0]["name"])
        playlist_dict["album"].append(track["album"]["name"])
        playlist_dict["id"].append(track["id"])
        playlist_dict["popularity"].append(track["popularity"])
        playlist_dict["duration"].append(track["duration_ms"])

    return pd.DataFrame(playlist_dict)


if __name__ == "__main__":
    # Request access token
    client_id = "73bec3d1dcc94665a5d4678d3429bf6f"
    client_secret = "50a3b18fb21b421a9e45fdb87f5c1f7f"
    access_token = auth_spotify(client_id, client_secret)
    print("token", access_token)

    # Get some artist data
    artist_id = "1eDIWVJt7ZWKsrXw5WVNsN?si=7b4c07a5bf5146ff"
    artist_response = get_artist(artist_id, access_token)

    # Get playlist data
    # playlist_id = "5XPDIbCZaBGHnlLfNqhQYk?si=12b0ebee4a674d39"
    playlist_id = "4jw7qBh5XcL7sT2AKgKg8R?si=12ed34e093cf4f78"
    playlist_response = get_playlist(playlist_id, access_token)

    playlist_df = playlist_to_df(playlist_response)
    playlist_df.to_csv("my_playlist.csv", index=False)

