# Streamlit

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.title("Spotify App")
Name_of_Artist = st.text_input("Artist Name")
Duration = st.number_input("Duration of playlist")
button_clicked = st.button("OK")

# Spotipy

from auth import *
from spotipy_client import *
import pandas as pd

client_id = cid
client_secret = secret

spotify = SpotifyAPI(client_id, client_secret)

Data = spotify.search({"artist": f"{Name_of_Artist}"}, search_type="track")

need = []
for i, item in enumerate(Data['tracks']['items']):
    track = item['album']
    track_id = item['id']
    song_name = item['name']
    popularity = item['popularity']
    duration = round(item['duration_ms'] / 60000, 0)
    need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity, duration))
 
Track_df = pd.DataFrame(need, index=None, columns=('Item', 'Artist', 'Album Name', 'Id', 'Song Name', 'Release Date', 'Popularity'))

access_token = spotify.access_token

headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/audio-features/"

st.table(Track_df[['Artist','Album Name', 'Song Name', 'Popularity', 'Duration (min)']])
