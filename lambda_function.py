import json
import os
from playlist_manager import PlaylistManager
from s3_manager import S3Manager
from json_manager import JsonManager
from env_manager import EnvManager
from spotify_top_tracks import SpotifyTopTracks
from spotify_top_artists_tracks import SpotifyTopArtistsTracks
from spotify_main import SpotifyMain

def lambda_handler(event, context):
    try:
        playlist_manager = PlaylistManager()
        s3_manager = S3Manager()
        json_manager = JsonManager()
        env_manager = EnvManager()
        spotify_top_tracks = SpotifyTopTracks(playlist_manager)
        spotify_top_artists_tracks = SpotifyTopArtistsTracks(playlist_manager)

        spotify_main = SpotifyMain(
            s3_manager,
            json_manager,
            env_manager,
            spotify_top_tracks,
            spotify_top_artists_tracks
        )

        spotify_main.run()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Success"})
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }