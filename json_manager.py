class JsonManager:

    def __init__(self):
        pass

    def make_new_user(self, data, username):
        data[username] = {
            "current_user_top_tracks_uris": {
                "short_term": '',
                "medium_term": '',
                "long_term": ''
            },
            "artist_top_tracks_uris": {
                "short_term": '',
                "medium_term": '',
                "long_term": ''
            }
        }
        return data
    
    def is_new_user(self, data, username):
        return username not in data