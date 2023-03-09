import boto3
import os
import json
from table_scan import mytablescan 
from functions import function_class

########## lambda function will triger when user request any method using API Gateway ##################################
def lambda_handler(event,context):
    function=function_class()
    response=""
    tablename = os.getenv('table_name')
    
    ### getting method name from event ###############################################################
    operation=event["httpMethod"]      #getting operation name from API Gatway request.
    #print(operation)   #print(url)




########### code for put item in url table ################################################################################    
    #https://dynobase.dev/dynamodb-python-with-boto3/#:~:text=To%20get%20all%20items%20from,the%20results%20in%20a%20loop
    if operation=="PUT":        #if operation is PUT then it will call the putmethod function from function file
        url=event['body']
        response=function.putmathod(url,operation,tablename,response)
        
        
        
        
        
        
########### code for delete item in url table ################################################################################  
    elif operation=="DELETE":                   #if operation is DELETE then it will call the putmethod function from function file
        response=url=event['body']
        response=function.deletemathod(url,operation,tablename,response)
        
        
        
        
        
        
        
########### code for get items in url table ###############################################################################################  
    elif operation=="GET":                     #if operation is GET then it will call the putmethod function from function file
        response=function.getmethod(operation,tablename,response)
        
        
        
        
        
        
########### code for update item in url table ################################################################################  
    elif operation=="POST":             #if operation is POST then it will call the putmethod function from function file
        url=event['body']
        response=function.postmethod(url,operation,tablename,response)
        
        
        
        
########### code for wrong selection ################################################################################      
    else:
        response="invalid request."
    
  
    return {'statusCode':200,
    'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': '*',
          },
    'body':json.dumps(response)}    
      

