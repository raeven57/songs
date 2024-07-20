from flask import Flask, request, jsonify
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

app = Flask(__name__)

# Replace these with your actual Spotify client ID and secret
CLIENT_ID = 'eb9fad1690b64f9a9b4f8bc8f2b93ebc'
CLIENT_SECRET = 'd8ce681159e94eed8bcdc7cfedc0bfae'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route('/recommend', methods=['GET'])
def recommend():
    song_id = request.args.get('song_id')

    if not song_id:
        return jsonify({'error': 'Song ID is required'}), 400

    try:
        recommendations = sp.recommendations(seed_tracks=[song_id], limit=10)
        recommended_tracks = []

        for track in recommendations['tracks']:
            track_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'preview_url': track['preview_url']
            }
            recommended_tracks.append(track_info)

        return jsonify(recommended_tracks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

