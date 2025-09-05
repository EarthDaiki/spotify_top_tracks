import json
from datetime import date

class PlaylistManager:

    def record_cuttu_playlist_uri(self, data, playlist_uri, term, username):
        '''
        update playlist uri data to store in a json file
        '''
        data[username]["current_user_top_tracks_uris"][term] = playlist_uri
        return data
    
    def record_attu_playlist_uri(self, data, playlist_uri, term, username):
        '''
        update playlist uri data to store in a json file
        '''
        data[username]["artist_top_tracks_uris"][term] = playlist_uri
        return data

    def save_playlist_uris(self, data):
        '''
        Save playlist uris (short, mid, and long terms) in a json file
        '''
        try:
            with open("Lambda\playlists_info.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("uris data is saved.")
        except Exception as e:
            print("uris data was not saved.", e)

    def get_songs_uri(self, sp, playlist_uri):
        '''
        get songs uris in a playlist
        '''
        prev_track_uris = []
        songs = sp.playlist_items(playlist_id=playlist_uri)
        for song in songs['items']:
            uri = song['track']['uri']
            prev_track_uris.append(uri)
        return prev_track_uris

    def get_my_playlists(self, sp):
        '''
        get user playlists
        '''
        results = sp.current_user_playlists()
        return results

    def make_playlist(self, sp, term, msg):
        '''
        make a term playlist
        '''
        today = date.today()
        new_playlist = sp.user_playlist_create(user=sp.me()['id'], name=f"{msg} {term}", public=False, collaborative=False, description=f'my {term} playlist on {today}')
        return new_playlist

    def delete_all_songs(self, sp, playlist_uri, prev_track_uris):
        '''
        delete all songs in a playlist to update it
        '''
        if prev_track_uris:
            sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_uri, items=prev_track_uris)

    def add_to_playlist(self, sp, track_uris, playlist_uri):
        sp.playlist_add_items(playlist_id=playlist_uri, items=track_uris)