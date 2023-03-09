import boto3
import json
class bucket3_class():

    def __init__(self):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html
        #session:A session stores configuration state and allows you to create service clients and resources.
        self.session = boto3.session.Session()
        #region_name (string) -- The name of the region associated with the client. A client is associated with a single region.
        self.current_region=self.session.region_name
        #client: service_name (string) -- The name of a service, e.g. 's3' or 'ec2'.
        self.s3_client=boto3.client('s3',region_name=self.current_region)
        #Session.resource(). Get a list of available services that can be loaded as resource clients
        self.resource=boto3.resource('s3',region_name=self.current_region)
        

    #take_data function download datta from s3 bucket and return the s3 bucket value
    def take_data(self,bucket_name,key):
        #bucket_name; the bucket_name specified the name of the bucket from where the data to be downloaded
        #key: the name of the file where the data is present.
        data=self.resource.Object(bucket_name=bucket_name,key=key)
        file=json.loads(data.get()['Body'].read().decode('utf-8'))
        return file