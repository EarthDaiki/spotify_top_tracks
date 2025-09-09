import spotipy
from spotipy.oauth2 import SpotifyOAuth
from s3_spotify_cache_handler import S3SpotifyCacheHandler
import os

class SpotifyMain:
    def __init__(self, s3_manager, json_manager, env_manager, spotify_top_tracks, spotify_top_artists_tracks):
        self.redirect_url = 'http://localhost:3000'
        self.scope = "user-read-recently-played user-read-playback-state user-top-read user-read-private user-library-read playlist-modify-private playlist-read-private user-modify-playback-state"
        self.s3_manager = s3_manager
        self.json_manager = json_manager
        self.env_manager = env_manager
        self.spotify_top_tracks = spotify_top_tracks
        self.spotify_top_artists_tracks = spotify_top_artists_tracks
    
    def run(self):
        user_info = self.env_manager.get_user_info()
        playlist_uri_data = self.s3_manager.load_info("daiki-spotify", "playlists_info.json")

        for username in user_info.keys():
            if self.json_manager.is_new_user(playlist_uri_data, username):
                playlist_uri_data = self.json_manager.make_new_user(playlist_uri_data, username)
            info = user_info[username]
            client_id = info['client_id']
            client_secret = info['client_secret']
        
            cache_handler = S3SpotifyCacheHandler(
                                s3_manager=self.s3_manager,
                                bucket="daiki-spotify",
                                key=f".cache-{username}"
                            )

            cache_data = cache_handler.get_cached_token()
            if cache_data is None:
                print(f"Skipping {username} because no token cache was found.")
                continue


            sp_auth = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                                  client_secret=client_secret,
                                                  redirect_uri=self.redirect_url,
                                                  scope=self.scope,
                                                  cache_handler=cache_handler,
                                                  show_dialog=True)

            sp = spotipy.Spotify(auth_manager=sp_auth)

            print(f"{sp.me()['display_name']} is now logged in.")

            self.spotify_top_tracks.main(sp, username, playlist_uri_data)
            self.spotify_top_artists_tracks.main(sp, username, playlist_uri_data)

            self.s3_manager.save_info("daiki-spotify", "playlists_info.json", playlist_uri_data)