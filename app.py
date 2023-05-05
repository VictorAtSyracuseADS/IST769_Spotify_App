import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd
from auth import cid, secret, username

# Set up Spotipy client
ccm = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=ccm)

os.environ["SPOTIPY_CLIENT_ID"] = cid
os.environ["SPOTIPY_CLIENT_SECRET"] = secret
os.environ["SPOTIPY_REDIRECT_URI"] = "https://localhost:8080"

scope = 'user-library-read playlist-modify-public'


token = spotipy.util.prompt_for_user_token(username, scope)

if token:
    spotipy_obj = spotipy.Spotify(auth=token)
    saved_tracks_resp = spotipy_obj.current_user_saved_tracks(limit=50)
else:
    print('Couldn\'t get token for that username')

# Define a function to generate song recommendations for a given track name


def generate_recommendations(track_name):
    # Search for the track using Spotipy and get its ID
    results = sp.search(q=f"track:{track_name}", type="track")
    track_id = results["tracks"]["items"][0]["id"]

    # Generate song recommendations using Spotipy
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=10)

    # Convert the recommendations to a pandas dataframe and select the relevant columns
    df = pd.DataFrame(recommendations["tracks"], columns=[
                      "id", "name", "artists", "popularity", "duration_ms"])
    df = df.rename(columns={"id": "track_id", "name": "track_name",
                   "artists": "artist_name", "duration_ms": "duration"})
    df["artist_name"] = df["artist_name"].apply(lambda x: x[0]["name"])
    df["duration"] = df["duration"].apply(lambda x: round(x / 60000, 2))

    return df.sort_values(by=['popularity', 'duration'], ascending=False)


# Define the Streamlit app
def app():
    st.title("Spotify Song Recommendations")

    # Prompt the user to enter a track name
    track_name = st.text_input("Enter a track name")

    # Generate recommendations and show the resulting table
    if track_name:
        df = generate_recommendations(track_name)
        total_duration = round(df['duration'].sum(), 0)
        st.write(f'Playlist length: {total_duration} minutes')
        st.table(df)

    # Add a button to regenerate the recommendations
    if st.button("Regenerate recommendations"):
        st.spinner("Generating recommendations...")
        df = generate_recommendations(track_name)
        st.table(df)


if __name__ == "__main__":
    app()
