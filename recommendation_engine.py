import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Spotify API credentials
client_id = '2385ab6617bf408e9cdd3438ebbd93dd'
client_secret = 'bea61dd1cb214d81928a581bbc9557ee'
redirect_uri = 'https://developer.spotify.com/dashboard/applications/2385ab6617bf408e9cdd3438ebbd93dd'

# Authenticate with required scopes
scope = "user-library-read user-read-recently-played user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Function to get user's saved tracks
def get_user_saved_tracks(limit=50):
    results = sp.current_user_saved_tracks(limit=limit)
    return [item['track'] for item in results['items']]

# Function to get user's top artists
def get_user_top_artists(limit=20):
    results = sp.current_user_top_artists(limit=limit, time_range='medium_term')
    return [artist['name'] for artist in results['items']]

# Function to recommend based on user's activity
def recommend_based_on_user_activity(user_id):
    saved_tracks = get_user_saved_tracks()
    top_artists = get_user_top_artists()

    # Example collaborative filtering: Recommend tracks based on top artists
    recommended_tracks = []
    for artist in top_artists:
        results = sp.search(q=f'artist:{artist}', type='track', limit=5)
        recommended_tracks.extend(results['tracks']['items'])

    # Example content-based filtering: Recommend tracks similar to saved tracks
    random_saved_track = random.choice(saved_tracks)
    track_features = sp.audio_features(tracks=[random_saved_track['id']])[0]
    recommendations_based_on_track = sp.recommendations(seed_tracks=[random_saved_track['id']], limit=5)

    return recommended_tracks, recommendations_based_on_track['tracks']

# Main program
if __name__ == "__main__":
    user_id = sp.current_user()['id']
    collab_filtering_recommendations, content_filtering_recommendations = recommend_based_on_user_activity(user_id)

    print("Collaborative Filtering Recommendations:")
    for track in collab_filtering_recommendations:
        print(f"- {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

    print("\nContent-Based Filtering Recommendations:")
    for track in content_filtering_recommendations:
        print(f"- {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")

