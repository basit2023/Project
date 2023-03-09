import boto3
from table_scan import mytablescan
#table_scan=mytablescan()
class function_class():
    def __init__(self):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html
        #create a dynamodb client
        self.client = boto3.client('dynamodb')
        #This class is take from table_scan
        self.table_scan=mytablescan()               
        
        
        
        
   ###############################m fucntion for putting items in the table ###########################################
   #The PUT method will put new value in the table, initally it will check if there is not the same value present
   #operation: consist the method by which we want to performed this operation (POST method here)
   #tablename: consit the name of the table where the value is present
   #response: simple string in which we want to return message
    def putmathod(self,url,operation,tablename,response):
        #this line will take all value of the table
         urls=self.table_scan.read_table(tablename) 
         ##This line will check if there is no same data in the table
         if url not in urls: 
            #put the value in the table 
            self.client.put_item(TableName= tablename,Item={'link':{'S' :url}})   
            response=response+"Item has been successfully putted into table."
            return response
         else:
            response=response+"Sorry!, The Item is already available in DynamoDB table. Try another."
            return response
            
            
            
            
            
  ####################################### deleting items from the table ########################################
    """
    The DELETE method will delete value from the table, first, it will check if there is same value present in the table
    Arg:
      operation: consist the method by which we want to performed this operation (POST method here)
      tablename: consit the name of the table where the value is present
      response: simple string in which we want to return message
    """
    def deletemathod(self,url,operation,tablename,response):
        #scan the table
        urls=self.table_scan.read_table(tablename)                                 
        if url in urls:  
            
            #if item exist in table
            #https://stackoverflow.com/questions/64187825/how-to-delete-all-the-items-in-the-dynamodb-with-boto3
            self.client.delete_item(TableName= tablename,Key={'link':{'S' : url}}) 
            response=response+"Item has been deleted from DynamoDB table."
            return response
        else:                    #if item not exist.
           response=response+"Sorry: The Item is not available in the table."
           return response
           
           
           
           
           
   ##################### geting items from the table #############################################################
    """
    The GET method will reat all table value, and will return all the value which is present in the table
    Arg:
      operation: consist the method by which we want to performed this operation (POST method here)
      tablename: consit the name of the table where the value is present
      response: simple string in which we want to return message
    """
    def getmethod(self,operation,tablename,response):      
        url=self.table_scan.read_table(tablename)           #search all data in the table
        response=url
        return response                                     #retun all the table value




   ######################### posting items in the table ###################################################
    """
    The Post method will update value in the table, if there is value present in the table
    Arg:
      operation: consist the method by which we want to performed this operation (POST method here)
      tablename: consit the name of the table where the value is present
      response: simple string in which we want to return message
    """
    def postmethod(self,url,operation,tablename,response):
        url_find=url.split(",")
        #the value which is present in the table
        old_url=url_find[0]    
        #new updated value
        new_url=url_find[1]   
        #read table
        urls=self.table_scan.read_table(tablename) 
        #if item is avaialble then update the value 
        if old_url in urls:                          
            self.client.delete_item(TableName= tablename,Key={'link':{'S' : old_url}})
            self.client.put_item(TableName= tablename,Item={'link':{'S' : new_url}})
            response+="Item has been updated in the table."
            return response
        else:                                   #incase item is not avaialble in table
            response=response+"Sorry! : The Item is not available in the DynamoDB table."
            return response
    