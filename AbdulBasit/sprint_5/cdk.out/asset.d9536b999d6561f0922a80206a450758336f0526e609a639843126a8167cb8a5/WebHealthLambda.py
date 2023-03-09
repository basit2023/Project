import urllib3                                                #these two are the builtin functions
import datetime
import boto3
import json
import sys
import os
#this class is imported form cloudwatch_put_metric
from cloudwatch_put_metric import Cloudwatch_putmetric
import constant as constant
#this class is imported form down_d_s3
#from S3_trigger_lambda.dow_d_s3 import bucket3_class
#this class is imported form put_Alarm
from Put_Alarm import Alarm
#cloudwatch client
client = boto3.client('cloudwatch')
#dynamodb client
client = boto3.client('dynamodb')
#import this class form API_lmbda folder table_scane file
from table_scan import mytablescan 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   S3 bucket download    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#s3=bucket3_class()
#file=s3.take_data('abdulbasitbucket','urls_for_bucket.json')



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   Lambda handler function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lambda_handler(event,context):
    """        Args: 
                  event(dict,optional): contains the data for a lambda fuction to process
                  context(object): passed by AWS lambda at runtime. contains methods and 
                  properties that provides information about the inocation, function,, and run time environment
    """
    
    #class imported from table_scan file
    table_scan=mytablescan()      
    # this line give us name of the table
    tablename = os.getenv('table_name') 
    #extric items from the table
    urls=table_scan.read_table(tablename)    
    sns_topic_arn = os.getenv('sns_topic_arn')

    
    
    
    
    
    
    #creating list for more urls data
    value=[]                                            
    
      
     
    #for loop is used to pickup multiful urs from constant.Url_to_monitor
    for url in urls:                                   
        
        avali=calc_avalibablity(url)
        latency=calc_latency(url)
        latency=calc_latency(url)
        Dimensions=[{
                    'Name': 'basit-urls',
                    'Value':url}]
        #class imported from cloudwatch_put_metri file
        cw=Cloudwatch_putmetric() 
        #Avalibality value pass to class           
        cw.put_matrics(constant.Namespace,constant.matric_name_avalibality,Dimensions,avali)
        #Latency value pass to class
        cw.put_matrics(constant.Namespace,constant.matric_name_latancy,Dimensions,latency)       
        ##https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
        put_A=Alarm()
        put_A.put_alarms(          #alarm name
                                   AlarmName="Basit_Alarm"+ " "+url,  
                                   #metric Name
                                   MetricName=constant.matric_name_avalibality,
                                   #name space
                                   Namespace=constant.Namespace,                       
                                   Statistic='Average',  
                                   #A dimension is a name/value pair that is part of the identity of a metric.
                                   Dimensions=Dimensions,
                                   #The length, in seconds, used each time the metric specified in MetricName is evaluated.
                                   Period=constant.period_alarm,
                                   #The number of periods over which data is compared to the specified threshold.
                                   EvaluationPeriods=constant.PERIOD,  
                                   #The value against which the specified statistic is compared.
                                   Threshold=constant.Threshold_Avalibality,
                                   #The arithmetic operation to use when comparing the specified statistic and threshold. 
                                   ComparisonOperator='GreaterThanOrEqualToThreshold', 
                                   AlarmActions=sns_topic_arn
                                   )
        
        value.append({"Avalibality":avali,"latency":latency})                  #append value to list
    return value
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   calculation avalibality    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
def calc_avalibablity(url):   
    #https://urllib3.readthedocs.io/en/latest/user-guide.html
    #this function is created for avalibality of the resorce
    #PoolManager instance to make requests.
    http = urllib3.PoolManager() 
    #if the resource is present then they will give the output 1.1 otherwise 0.0
    request = http.request('GET', url)   
    if request.status==200:
        return 1.0
    else:
        return 0.0
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   calculation latency   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def calc_latency(url):                          #this function will calculate the latency for a specific website
    http = urllib3.PoolManager()
    #noted time just before the runing url
    start = datetime.datetime.now()   
    #url will run form this line
    request = http.request('GET', url) 
    #noted time just after the url responding
    end = datetime.datetime.now()  
    # #time different between them
    diff = end - start       
    #rounding of the time
    return round(diff.microseconds * .000001, 6)      




    
  