import urllib3                                                #these two are the builtin functions
import datetime
import json
import boto3
import os
def LambdaApps(event,context):
    http = urllib3.PoolManager() 
    # boto3
    s3=boto3.client("s3")
    if event:
        bucketname=os.getenv('bucket')
        file_obj=event["Records"][0]
        bucket_name=str(file_obj["s3"]["bucket"]["name"])
        file_name=str(file_obj["s3"]["object"]["key"])
        print("file name : ",file_name)
        fileObj=s3.get_object(Bucket=bucket_name,key=file_name)
        file_content=fileObj["body"].read().decode("utf-8")
        print(file_content)
    
    
    
    
    
    data={ "text":"simple message form lambda"}
    request = http.request('POST','https://hooks.slack.com/services/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',
                           body=json.dumps(data), headers={"Content-Type":"application/json"})   
    return {'statusCode':200,'body':'Hello from lambda'}
    