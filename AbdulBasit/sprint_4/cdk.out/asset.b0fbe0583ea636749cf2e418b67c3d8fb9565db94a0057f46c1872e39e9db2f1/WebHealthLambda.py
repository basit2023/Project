import urllib3                                                #these two are the builtin functions
import datetime
import boto3
import json
import sys
import os
from cloudwatch_put_metric import Cloudwatch_putmetric
import constant as constant
from dow_d_s3 import bucket3_class
from Put_Alarm import Alarm
client = boto3.client('cloudwatch')
client = boto3.client('dynamodb')
from table_scan import mytablescan 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   S3 bucket download    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# session = boto3.session.Session()
# current_region=session.region_name
# s3_client=boto3.client('s3',region_name=current_region)
# s3_client=boto3.client('s3')  
# resource=boto3.resource('s3',region_name=current_region)
# data=resource.Object(bucket_name='bucket-for-url',key='urls_for_bucket.json')
# file=json.loads(data.get()['Body'].read().decode('utf-8'))
# s3_client.download_file('bucket-for-url','urls_for_bucket.json', '/tmp/constan_t.json')
# sys.path.insert(1,'/tmp')
#import constan_t
#print(constan_t.values())


s3=bucket3_class()
file=s3.take_data('abdulbasitbucket','urls_for_bucket.json')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   Lambda handler function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lambda_handler(event,context):
    """        Args: 
                  event(dict,optional): contains the data for a lambda fuction to process
                  context(object): passed by AWS lambda at runtime. contains methods and 
                  properties that provides information about the inocation, function,, and run time environment
    """
    
    
    table_scan=mytablescan()                 #class imported from table_scan file
    tablename = os.getenv('table_name')      # this line give us name of the table
    urls=table_scan.read_table(tablename)    #extric items from the table
    sns_topic_arn = os.getenv('sns_topic_arn')

    
    
    
    
    
    
    
    value=[]                                            #creating list for more urls data
    
    put_A=Alarm()          
    cw=Cloudwatch_putmetric()                           #class imported from cloudwatch_put_metri file 
    for url in urls:                                   #for loop is used to pickup multiful urs from constant.Url_to_monitor
        
        avali=calc_avalibablity(url)
        latency=calc_latency(url)
        latency=calc_latency(url)
        Dimensions=[{
                    'Name': 'basit-url',
                    'Value':url}]
                    
        cw.put_matrics(constant.Namespace,constant.matric_name_avalibality,Dimensions,avali)    #Avalibality value pass to class
        cw.put_matrics(constant.Namespace,constant.matric_name_latancy,Dimensions,latency)       #Avalibality value pass to class
        
        put_A.put_alarms(          AlarmName="Basit_Alarm"+ " "+url,                   #alarm name
                                   MetricName=constant.matric_name_avalibality,        #metric Name
                                   Namespace=constant.Namespace,                       #name space
                                   Statistic='Average',                                
                                   Dimensions=Dimensions,                              #A dimension is a name/value pair that is part of the identity of a metric.
                                   Period=10,                                          #The length, in seconds, used each time the metric specified in MetricName is evaluated.
                                   EvaluationPeriods=constant.PERIOD,                  #The number of periods over which data is compared to the specified threshold.
                                   Threshold=constant.Threshold_Avalibality,           #The value against which the specified statistic is compared.
                                   ComparisonOperator='GreaterThanOrEqualToThreshold', #The arithmetic operation to use when comparing the specified statistic and threshold. 
                                   AlarmActions=sns_topic_arn
                                   )
        
        value.append({"Avalibality":avali,"latency":latency})                  #append value to list
    return value
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   calculation avalibality    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
def calc_avalibablity(url):                         #this function is created for avalibality of the resorce
    http = urllib3.PoolManager()                    #if the resource is present then they will give the output 1.1 otherwise 0.0
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
    start = datetime.datetime.now()             #noted time just before the runing url
    request = http.request('GET', url)          #url will run form this line
    end = datetime.datetime.now()               #noted time just after the url responding
    diff = end - start                          #time different between them
    return round(diff.microseconds * .000001, 6)      #rounding of the time




    
  