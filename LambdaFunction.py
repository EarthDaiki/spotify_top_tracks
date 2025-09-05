import json
import os
from spotify_top_tracks import SpotifyTopTracks
from spotify_top_artists import SpotifyTopArtistsTracks
from playlist_manager import PlaylistManager
from json_manager import JsonManager

if __name__ == '__main__':
    playlist_manager = PlaylistManager()
    json_manager = JsonManager()
    stp = SpotifyTopTracks(playlist_manager, json_manager)
    stp.main()
    stat = SpotifyTopArtistsTracks(playlist_manager, json_manager)
    stat.main()