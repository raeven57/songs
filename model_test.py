import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

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


# Function to get user's top artists
def get_user_top_artists(limit=20):
    results = sp.current_user_top_artists(limit=limit, time_range='medium_term')
    return [artist['name'] for artist in results['items']]


# Example collaborative filtering: Recommend tracks based on top artists
def recommend_tracks_collaborative(user_id):
    top_artists = get_user_top_artists()
    recommended_tracks = []

    for artist in top_artists:
        results = sp.search(q=f'artist:{artist}', type='track', limit=5)
        recommended_tracks.extend(results['tracks']['items'])

    # Sort recommended tracks by popularity (descending)
    recommended_tracks.sort(key=lambda x: x['popularity'], reverse=True)

    return recommended_tracks[:10]  # Limit to top 10 tracks for better visibility


# Example content-based filtering: Recommend tracks based on audio features
def recommend_tracks_content_based(user_id):
    saved_tracks = get_user_saved_tracks()
    random_track = saved_tracks[0]  # Example: Selecting the first saved track
    track_id = random_track['id']

    recommendations = sp.recommendations(seed_tracks=[track_id], limit=10)
    return recommendations['tracks']


# Function to get user's saved tracks
def get_user_saved_tracks(limit=50):
    results = sp.current_user_saved_tracks(limit=limit)
    return [item['track'] for item in results['items']]


# Main program
if __name__ == "__main__":
    user_id = sp.current_user()['id']

    # Collaborative filtering recommendations
    collab_recommendations = recommend_tracks_collaborative(user_id)

    # Plotting collaborative filtering recommendations
    plt.figure(figsize=(10, 6))
    plt.barh([track['name'] for track in collab_recommendations[::-1]],
             [track['popularity'] for track in collab_recommendations[::-1]],
             color='b')
    plt.xlabel('Popularity')
    plt.title('Top Collaborative Filtering Recommendations')
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.tight_layout()
    plt.show()

    # Content-based filtering recommendations
    content_recommendations = recommend_tracks_content_based(user_id)

    # Plotting content-based filtering recommendations
    plt.figure(figsize=(10, 6))
    plt.barh([track['name'] for track in content_recommendations[::-1]],
             [track['popularity'] for track in content_recommendations[::-1]],
             color='g')
    plt.xlabel('Popularity')
    plt.title('Top Content-Based Filtering Recommendations')
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    user_id = sp.current_user()['id']

    # Get recommended tracks
    collab_recommendations = recommend_tracks_collaborative(user_id)

    # Calculate average popularity of recommended tracks
    total_popularity = sum(track['popularity'] for track in collab_recommendations)
    average_popularity = total_popularity / len(collab_recommendations)

    # Print results
    print(f"Average Popularity of Recommended Tracks: {average_popularity}")