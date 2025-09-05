import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

from dotenv import dotenv_values

class SpotifyTopTracks:
    def __init__(self, playlist_manager, json_manager):
        self.redirect_url = 'http://localhost:3000'
        self.scope = "user-read-recently-played user-read-playback-state user-top-read user-read-private user-library-read playlist-modify-private playlist-read-private user-modify-playback-state"
        self.playlist_manager = playlist_manager
        self.json_manager = json_manager
        
    
    def update_playlist(self, sp, term, prev_track_uris, playlist_uri):
        '''
        update a playlist. If a playlist is the same as previous version, this function does nothing.
        However, if a playlist is not the same as previous one, all songs in the playlist will be deleted and add new songs.
        '''
        track_uris = []
        results = sp.current_user_top_tracks(limit=20, offset=0, time_range=term)
        for number, result in enumerate(results['items']):
            # print(result['name'])
            uri = result['uri']
            track_uris.append(uri)
        if prev_track_uris == track_uris:
            return False
        else:
            self.playlist_manager.delete_all_songs(sp, playlist_uri, prev_track_uris)
            self.playlist_manager.add_to_playlist(sp, track_uris, playlist_uri)
            return True
    
    def main(self):

        config = dict(dotenv_values("Lambda/.env"))
        
        user_info = {
            'Daiki': {
                'client_id': config['DaikiClientId'],
                'client_secret': config['DaikiClientSecret']
            }
        }

        with open("Lambda\playlists_info.json", "r", encoding="utf-8") as f:
            data = json.load(f)

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

            my_playlists = self.playlist_manager.get_my_playlists(sp)

            if self.json_manager.is_new_user(data, username):
                self.json_manager.make_new_user(data, username)

            for term, recorded_playlist_uri in list(data[username]["current_user_top_tracks_uris"].items()):
                for my_playlist in my_playlists['items']:
                    # if recored playlist uri's playlist does not exist, create a new playlist.
                    if recorded_playlist_uri == my_playlist['uri']:
                        print(f'top song {term} exists')
                        break
                else:
                    my_playlist = self.playlist_manager.make_playlist(sp, term, "top songs")
                    data = self.playlist_manager.record_cuttu_playlist_uri(data, my_playlist['uri'], term, username)
                    print(f"top song {term} made")
                    prev_track_uris = self.playlist_manager.get_songs_uri(sp, my_playlist['uri'])
                    if self.update_playlist(sp, term, prev_track_uris, my_playlist['uri']):
                        print(f"{term} modified!:heart_eyes:")
                    self.playlist_manager.save_playlist_uris(data)
            