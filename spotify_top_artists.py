import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import dotenv_values

class SpotifyTopArtistsTracks:
    def __init__(self, playlist_manager, json_manager):
        self.redirect_url = 'http://localhost:3000'
        self.scope = "user-read-recently-played user-read-playback-state user-top-read user-read-private user-library-read playlist-modify-private playlist-read-private user-modify-playback-state"
        self.playlist_manager = playlist_manager
        self.json_manager = json_manager

    def get_top_artists(self, sp, term):
        result = sp.current_user_top_artists(limit=20, offset=0, time_range=term)
        return result
    
    def get_top_artists_tracks(self, sp, artist_id):
        result = sp.artist_top_tracks(artist_id)
        return result
    
    def update_playlist(self, sp, playlist_uri, term, prev_track_uris):
        artists = self.get_top_artists(sp, term)
        playlist_tracks = []
        for artist in artists['items']:
            tracks = self.get_top_artists_tracks(sp, artist['id'])
            for track in tracks['tracks']:
                playlist_tracks.append(track['uri'])
        if prev_track_uris == playlist_tracks:
            return False
        else:
            for i in range(0, len(prev_track_uris), 100):
                self.playlist_manager.delete_all_songs(sp, playlist_uri, prev_track_uris[i:i+100])
            for i in range(0, len(playlist_tracks), 100):
                self.playlist_manager.add_to_playlist(sp, playlist_tracks[i:i+100], playlist_uri)
            return True

    def main(self):

        config = dict(dotenv_values("Lambda/.env"))
        
        user_info = {
            'Daiki': {
                'client_id': config['DaikiClientId'],
                'client_secret': config['DaikiClientSecret']
            }
        }

        for username in user_info.keys():
            info = user_info[username]
            client_id = info['client_id']
            client_secret = info['client_secret']
        
            cache_handler = spotipy.cache_handler.CacheFileHandler(username=username)
            sp_auth = spotipy.oauth2.SpotifyOAuth(client_id=client_id,
                                                  client_secret=client_secret,
                                                  redirect_uri=self.redirect_url,
                                                  scope=self.scope,
                                                  cache_handler=cache_handler,
                                                  show_dialog=True)
            sp = spotipy.Spotify(auth_manager=sp_auth)
        
            print(sp.me()['display_name'])

            with open("Lambda\playlists_info.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            my_playlists = self.playlist_manager.get_my_playlists(sp)

            if self.json_manager.is_new_user(data, username):
                self.json_manager.make_new_user(data, username)

            for term, recorded_playlist_uri in list(data[username]["artist_top_tracks_uris"].items()):
                for my_playlist in my_playlists['items']:
                    if recorded_playlist_uri == my_playlist['uri']:
                        print(f'top artist song {term} exists')
                        break
                else:
                    my_playlist = self.playlist_manager.make_playlist(sp, term, "top artists")
                    data = self.playlist_manager.record_attu_playlist_uri(data, my_playlist['uri'], term, username)
                    print(f"top artist song {term} made")
                    prev_track_uris = self.playlist_manager.get_songs_uri(sp, my_playlist['uri'])
                    if self.update_playlist(sp, my_playlist['uri'], term, prev_track_uris):
                        print(f"{term} modified!:heart_eyes:")
                    self.playlist_manager.save_playlist_uris(data)