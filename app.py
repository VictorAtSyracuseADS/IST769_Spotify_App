# Streamlit App

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.title("Spotify App")
Name_of_Playlist = st.text_input("Enter type of playlist")
Duration_Range = st.slider(label="Duration of playlist in minutes", min_value = 4, max_value = 180, value = (60, 80), help = "Choose a range of the playlist length using minutes")
button_clicked = st.button("OK")

# Spotify API

from auth import *
from spotipy_client import *
import pandas as pd

client_id = cid
client_secret = secret

spotify = SpotifyAPI(client_id, client_secret)

Data = spotify.search({"playlist": f"{Name_of_Playlist}"}, search_type="track")

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

current_dur = 0
data = []

if button_clicked:
    for i, row in Track_df.sort_values(by="Popularity", ascending = False).iterrows():
        if Duration_Range[1] > current_dur:
            artist = row['Artist']
            song = row['Song Name']
            pop = row['Popularity']
            dur = row['Duration']                        
            data.append((artist, song, pop, dur))
            current_dur += int(row['Duration'])
        else:
            current_dur = 0
            break

# Show the result from the filter
Result_df = pd.DataFrame(data, index=None, columns=('Artist', 'Song Name', 'Popularity', 'Duration'))

st.table(Result_df[['Artist', 'Song Name', 'Popularity', 'Duration']])
