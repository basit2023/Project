import boto3
from table_scan import mytablescan
#table_scan=mytablescan()
class function_class():
    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.table_scan=mytablescan()               #This class is take from table_scan
        
        
        
        
   ###############################m fucntion for putting items in the table ###########################################
   
    def putmathod(self,url,operation,tablename,response):
         urls=self.table_scan.read_table(tablename)              
         if url not in urls:
            self.client.put_item(TableName= tablename,Item={'link':{'S' :url}})
            response=response+"Item has been successfully putted into table."
            return response
         else:
            response=response+"Sorry!, The Item is already available in DynamoDB table. Try another."
            return response
            
            
            
            
            
  ####################################### deleting items from the table ########################################
    def deletemathod(self,url,operation,tablename,response):
        urls=self.table_scan.read_table(tablename)
        if url in urls:       #if item exist in table
           self.client.delete_item(TableName= tablename,Key={'link':{'S' : url}}) #https://stackoverflow.com/questions/64187825/how-to-delete-all-the-items-in-the-dynamodb-with-boto3
           response=response+"Item has been deleted from DynamoDB table."
           return response
        else:                    #if item not exist.
           response=response+"Sorry: The Item is not available in the table."
           return response
           
           
           
           
           
   ##################### geting items from the table #############################################################
    def getmethod(self,operation,tablename,response):
        url=self.table_scan.read_table(tablename)
        response=url
        return response




   ######################### posting items in the table ###################################################
    def postmethod(self,url,operation,tablename,response):
        url_find=url.split(",")
        old_url=url_find[0]
        new_url=url_find[1]
        urls=self.table_scan.read_table(tablename)  #read table
        if old_url in urls:                 #if item is avaialble then 
            self.client.delete_item(TableName= tablename,Key={'link':{'S' : old_url}})
            self.client.put_item(TableName= tablename,Item={'link':{'S' : new_url}})
            response+="Item has been updated in the table."
            return response
        else:                                   #incase item is not avaialble in table
            response=response+"Sorry! : The Item is not available in the DynamoDB table."
            return response
    