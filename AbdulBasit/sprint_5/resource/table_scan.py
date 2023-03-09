

import boto3
############### to read all url from table and  return list of url #######################################
class mytablescan:
    def read_table(self,table_name):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
        client = boto3.client('dynamodb')
        
        
        ####### get all data by scan function ########################################
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan
        #taking data from the table
        table_data = client.scan(TableName=table_name,AttributesToGet=['link'])                
        
        
        
        ######## extract url from array of dictionary ##########################
        url=table_data["Items"]
        
        
        
        ######### converting dictionary to array of string ##################
        for n in range(len(url)):
            url[n]=url[n]['link']['S']
            
            
            
            
            
            
        # if no url in table  return message 
        if len(url)==0:
            return "Table has not Items(URL)"
        #if url are vaialble then return list of url
        return url
