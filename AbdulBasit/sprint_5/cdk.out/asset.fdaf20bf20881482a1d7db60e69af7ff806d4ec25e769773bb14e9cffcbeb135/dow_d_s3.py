import boto3
import json
class bucket3_class():
    def __init__(self):
        self.session = boto3.session.Session()
        self.current_region=self.session.region_name
        self.s3_client=boto3.client('s3',region_name=self.current_region)
        self.resource=boto3.resource('s3',region_name=self.current_region)
        
        
    def take_data(self,bucket_name,key):
        data=self.resource.Object(bucket_name=bucket_name,key=key)
        file=json.loads(data.get()['Body'].read().decode('utf-8'))
        return file