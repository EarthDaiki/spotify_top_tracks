import os

class EnvManager:
    def __init__(self):
        pass

    def get_user_info(self):
        # This os.environ is getting from lambda env variables.
        user_info = {
            'Daiki': {
                'client_id': os.environ['DaikiClientId'],
                'client_secret': os.environ['DaikiClientSecret']
            }
        }
        return user_info