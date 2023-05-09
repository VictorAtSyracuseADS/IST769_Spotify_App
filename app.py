# Streamlit App

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.title("Spotify App")
Name_of_Artist = st.text_input("Artist Name")
Duration = st.number_input("Duration of playlist in minutes", min_value = 1, value = 30, step = 1, help = "Enter the length of the playlist using minutes")
button_clicked = st.button("OK")

# Spotify API

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
    duration = item['duration_ms']
    need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity, duration))
 
Track_df = pd.DataFrame(need, index=None, columns=('Item', 'Artist', 'Album Name', 'Id', 'Song Name', 'Release Date', 'Popularity', 'Duration'))

def convert_ms(duration):
    minutes = round(duration / 60000, 1)
    return minutes 

Track_df['Duration'] = Track_df['Duration'].apply(convert_ms)

Result_df = Track_df.loc[:,Track_df['Duration'].sum() < Duration].sort_values(by="Popularity")

st.table(Result_df[['Artist','Album Name', 'Song Name', 'Popularity', 'Duration']])
