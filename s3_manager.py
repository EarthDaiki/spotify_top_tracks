import json
import boto3
import os

class S3Manager:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def load_info(self, bucket_name, key):
        try:
            obj = self.s3.get_object(Bucket=bucket_name, Key=key)
            data = obj["Body"].read().decode("utf-8")
            return json.loads(data)
        except self.s3.exceptions.NoSuchKey:
            print("No cache found in S3.")
            return {}

    def save_info(self, bucket_name, key, data):
        try:
            self.s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=json.dumps(data, ensure_ascii=False, indent=4),
                ContentType="application/json"
            )
        except self.s3.exceptions.NoSuchKey:
            print("could not save.")