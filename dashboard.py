import streamlit as st
import playlists, authorization


if __name__ == "__main__":
    st.title("Spotify playlist visualization")

    # initialize (get access token)
    access_token = authorization.auth_spotify(*authorization.load_secrets())

    playlist_dict = playlists.load_playlists(playlists.id_list, access_token)
    ids_names = playlists._ids_to_names(playlist_dict)

    playlist_name = st.selectbox("Select a playlist", ids_names.keys())

    playlist_df = playlists.playlist_to_df(playlist_dict[ids_names[playlist_name]])

    st.dataframe(playlist_df)
