"""
Manage playlists
"""
import pandas as pd
import requests

id_list = ["4jw7qBh5XcL7sT2AKgKg8R?si=12ed34e093cf4f78",
           "2gs2XjbCKNQg7ImWR0MBBh?si=7a698a84367549a3"]


def load_playlists(id_list, access_token):
    playlist_dict = {}
    for id in id_list:
        playlist_dict[id] = get_playlist(id, access_token)
    return playlist_dict


# TODO: rename to "names_to_ids"?
def _ids_to_names(playlist_dict):
    d = {}
    for k in playlist_dict.keys():
        d[playlist_dict[k]['name']] = k
    return d


def get_playlist(playlist_id, access_token):
    header = {'Authorization': f"Bearer {access_token}"}
    URl = f'https://api.spotify.com/v1/playlists/{playlist_id}'

    response = requests.get(URl, headers=header)
    return response.json()


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
