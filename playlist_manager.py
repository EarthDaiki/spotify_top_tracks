import json

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

    def make_playlist(self, sp, name, public=False, collaborative=False, description=None):
        '''
        make a term playlist
        '''
        new_playlist = sp.user_playlist_create(user=sp.me()['id'], name=name, public=public, collaborative=collaborative, description=description)
        return new_playlist

    def delete_all_songs(self, sp, playlist_uri, prev_track_uris):
        '''
        delete all songs in a playlist to update it
        '''
        if prev_track_uris:
            sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_uri, items=prev_track_uris)

    def add_to_playlist(self, sp, track_uris, playlist_uri):
        sp.playlist_add_items(playlist_id=playlist_uri, items=track_uris)

    def change_playlist_details(self, sp, playlist_uri, name=None, public=None, collaborative=None, description=None):
        '''
        change playlist details
        '''
        sp.playlist_change_details(playlist_id=playlist_uri, name=name, public=public, collaborative=collaborative, description=description)