
import boto3
class DynamoDB_class():
    def __init__(self):
        self.client=boto3.client('dynamodb')    #create a boto3 client
        
        
    def insert_data_for_table(self,table_name,message):    #this function is call from db_lambda file
        """
        Arg:
        TableName: it consist the name of the table 
        Item: it consit the data which we want to put into table.
        """
        response=self.client.put_item(TableName= table_name,Item=message)    #this line will put value into table
        return response

