from datetime import date

class SpotifyTopTracks:
    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager
        
    
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
    
    def main(self, sp, username, playlist_uri_data):
        today = date.today()
        my_playlists = self.playlist_manager.get_my_playlists(sp)

        for term, recorded_playlist_uri in list(playlist_uri_data[username]["current_user_top_tracks_uris"].items()):
            print(f"=====top song {term}=====")
            for my_playlist in my_playlists['items']:
                # if recored playlist uri's playlist does not exist, create a new playlist.
                if recorded_playlist_uri == my_playlist['uri']:
                    print('playlist exists.')
                    self.playlist_manager.change_playlist_details(sp, my_playlist['uri'], description=f'my {term} playlist on {today}')
                    print("details are changed.")
                    break
            else:
                my_playlist = self.playlist_manager.make_playlist(sp, name=f'{term} top tracks', description=f'my {term} playlist on {today}')
                playlist_uri_data = self.playlist_manager.record_cuttu_playlist_uri(playlist_uri_data, my_playlist['uri'], term, username)
                print("playlist is made.")

            prev_track_uris = self.playlist_manager.get_songs_uri(sp, my_playlist['uri'])
            if self.update_playlist(sp, term, prev_track_uris, my_playlist['uri']):
                print("modified")
            else:
                print("NOT modified.")
            