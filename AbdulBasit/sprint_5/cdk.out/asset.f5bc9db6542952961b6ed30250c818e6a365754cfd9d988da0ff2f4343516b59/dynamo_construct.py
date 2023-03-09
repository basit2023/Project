
import boto3
class DynamoDB_class():
    def __init__(self):
        self.client=boto3.client('dynamodb')
        
        
    def insert_data_for_table(self,table_name,message):
        
        response=self.client.put_item(TableName= table_name,Item=message)
        return response

