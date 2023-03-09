
from dynamo_construct import DynamoDB_class

import os
import json
def lambda_handler(event,context):

    #this function return the record to table
    
    db=DynamoDB_class()
   
    #messageid=event["Records"][0]["Sns"]["MessageId"]
    time_stamp=event["Records"][0]["Sns"]["Timestamp"]
    #time_stamp = json.loads(time_stamp)
    messageid=event["Records"][0]["Sns"]["MessageId"]
    subject=event['Records'][0]['Sns']['Subject']
    message=event['Records'][0]['Sns']['Message']
    table_name=os.getenv("table_name")
    data={
            'Timestamp':time_stamp,
            'MessageId':messageid,
            'Subject':subject,
            'Message':[message,]
           
          }
    db.insert_data_for_table(table_name,data)
    #db.read_data(table_name,data)
    
    
    
    