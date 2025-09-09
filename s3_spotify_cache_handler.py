import json
from spotipy.cache_handler import CacheHandler

class S3SpotifyCacheHandler(CacheHandler):
    def __init__(self, s3_manager, bucket, key):
        self.s3_manager = s3_manager
        self.bucket = bucket
        self.key = key
        self.cache_data = self._load_from_s3()

    def _load_from_s3(self):
        cache_data = self.s3_manager.load_info(self.bucket, self.key)
        return cache_data

    def get_cached_token(self):
        if self.cache_data is None:
            print(f"[INFO] No cache found for {self.key}.")
            return None 
        return self.cache_data

    def save_token_to_cache(self, token_info):
        self.cache_data = token_info
        self.s3_manager.save_info(self.bucket, self.key, token_info)