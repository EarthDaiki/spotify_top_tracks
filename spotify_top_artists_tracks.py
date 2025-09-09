from datetime import date

class SpotifyTopArtistsTracks:
    def __init__(self, playlist_manager):
        self.playlist_manager = playlist_manager

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

    def main(self, sp, username, playlist_uri_data):
        today = date.today()
        my_playlists = self.playlist_manager.get_my_playlists(sp)

        for term, recorded_playlist_uri in list(playlist_uri_data[username]["artist_top_tracks_uris"].items()):
            print(f"=====top artists {term}=====")
            for my_playlist in my_playlists['items']:
                if recorded_playlist_uri == my_playlist['uri']:
                    print('playlist exists.')
                    self.playlist_manager.change_playlist_details(sp, my_playlist['uri'], description=f'my {term} playlist on {today}')
                    print("details are changed.")
                    break
            else:
                my_playlist = self.playlist_manager.make_playlist(sp, name=f'{term} top artists tracks', description=f'my {term} playlist on {today}')
                playlist_uri_data = self.playlist_manager.record_attu_playlist_uri(playlist_uri_data, my_playlist['uri'], term, username)
                print("playlist is made.")

            prev_track_uris = self.playlist_manager.get_songs_uri(sp, my_playlist['uri'])
            if self.update_playlist(sp, my_playlist['uri'], term, prev_track_uris):
                print("modified")
            else:
                print("NOT modified")