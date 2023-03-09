import json
import boto3
import os
from dow_d_s3 import bucket3_class
import constant as constant 
#Class is imported from lag_store_lambda, dynamo_construct file
from Log_store_lambda.dynamo_construct import DynamoDB_class
def lambda_handler(event,context):
    value = dict()
############ getting bucket name and file name from even ###########################################################
    bucketname = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    bucketname=os.getenv('bucket')
    filename="urls_for_bucket.json"
#################getting url list from s3 bucket and writing into dynamo DB table ####################################


    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
    client = boto3.client('dynamodb')
    #this class is imported from dow_d_s3 file
    s3=bucket3_class()                                          
    s3_data=s3.take_data(bucketname,filename)   
    #getting table name
    tablename = os.getenv('table_name')   
    #this class is imported from dynamo_construct file
    db=DynamoDB_class()                                       
    for i in s3_data:
        data={'link':{'S' : s3_data[i]}}
        db.insert_data_for_table(tablename,data)