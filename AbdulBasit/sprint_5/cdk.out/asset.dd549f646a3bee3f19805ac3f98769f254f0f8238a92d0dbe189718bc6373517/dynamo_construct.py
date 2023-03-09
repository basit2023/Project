
import boto3
class DynamoDB_class():
    def __init__(self):
        self.session = boto3.session.Session()
        self.current_region=self.session.region_name
        self.client=boto3.client('dynamodb',region_name=self.current_region)
        
        
        
    def insert_data_for_table(self,table_name,message):
        #name of the table
        #table=self.client.Table(table_name)   
        #puting data into table
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item
        response=self.client.put_item(TableName= table_name,Item=message)
        return response

