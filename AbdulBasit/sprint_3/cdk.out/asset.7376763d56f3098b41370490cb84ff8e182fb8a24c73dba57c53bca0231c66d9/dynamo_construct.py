import boto3
class DynamoDB_class():
    def __init__(self):
        self.session = boto3.session.Session()
        self.current_region=self.session.region_name
        self.resource=boto3.resource('dynamodb',region_name=self.current_region)
        
        
        
    def insert_data_for_table(self,table_name,message):
        table=self.resource.Table(table_name)
        response=table.put_item(Item=message)
        return response



