# OOP WITH PYTHON ASSIGNMENT 3

# *** QUESTION 5 ***
print("\n\n*** QUESTION 5 ***\n\n")


import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import random


class UgandaMusicAnalytics:
    def __init__(self, use_mock=True, client_id=None, client_secret=None):
        self.use_mock = use_mock
        self.results = []
        self.artists = ["Azawi", "Sheebah", "Eddy Kenzo", "Bebe Cool", "Spice Diana"]

        if not use_mock:
            try:
                self.sp = Spotify(auth_manager=SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                ))
            except SpotifyException as e:
                raise ConnectionError("Spotify API token error. Check your credentials.") from e

    def fetch_top_tracks(self):
        if self.use_mock:
            self.results = self.load_mock_data()
        else:
            for artist in self.artists:
                try:
                    search = self.sp.search(q=artist, type='artist', limit=1)
                    if search['artists']['items']:
                        artist_id = search['artists']['items'][0]['id']
                        top_tracks = self.sp.artist_top_tracks(artist_id)['tracks']
                        for track in top_tracks:
                            self.results.append({
                                "artist": artist,
                                "track": track['name'],
                                "popularity": track['popularity'],
                                "play_count": random.randint(10_000, 500_000),  # Simulated play count
                                "country": "Uganda" if random.random() > 0.2 else "Other"  # 80% Uganda
                            })
                except SpotifyException as e:
                    print(f"Spotify error while fetching {artist}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

    def load_mock_data(self):
        return [
            {"artist": "Azawi", "track": "Repeat It", "popularity": 70, "play_count": 120000, "country": "Uganda"},
            {"artist": "Sheebah", "track": "Nakyuka", "popularity": 65, "play_count": 100000, "country": "Uganda"},
            {"artist": "Eddy Kenzo", "track": "Sitya Loss", "popularity": 75, "play_count": 500000, "country": "Uganda"},
            {"artist": "Bebe Cool", "track": "Break the Chains", "popularity": 68, "play_count": 250000, "country": "Uganda"},
            {"artist": "Spice Diana", "track": "Kwata Wano", "popularity": 62, "play_count": 90000, "country": "Other"},
        ]

    def to_dataframe(self):
        return pd.DataFrame(self.results)

    def plot_popularity(self, df):
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x="track", y="popularity", hue="artist", dodge=False)
        plt.title("Track Popularity of Ugandan Artists")
        plt.ylabel("Popularity (Spotify Score)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def save_to_json(self, filename="ugandan_tracks.json"):
        try:
            with open(filename, "w") as f:
                json.dump(self.results, f, indent=4)
            print(f"Saved data to {filename}")
        except Exception as e:
            print(f"Error saving JSON: {e}")


class LocalArtistAnalytics(UgandaMusicAnalytics):
    def get_uganda_only_tracks(self):
        return [track for track in self.results if track.get("country") == "Uganda"]


# === Run Analytics ===
if __name__ == "__main__":
    # Set use_mock=False and provide client_id/secret if using Spotify API

    analytics = LocalArtistAnalytics(use_mock=True)

    analytics.fetch_top_tracks()
    ugandan_tracks = analytics.get_uganda_only_tracks()

    df = pd.DataFrame(ugandan_tracks)
    print("\n=== Ugandan Produced Tracks ===")
    print(df[["artist", "track", "popularity", "play_count"]])

    analytics.plot_popularity(df)
    analytics.save_to_json("ugandan_tracks_filtered.json")
