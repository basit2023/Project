import urllib3                                                #these two are the builtin functions
import datetime
import boto3
import sys
from cloudwatch_put_metric import Cloudwatch_putmetric
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   S3 bucket download    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

s3_client=boto3.client('s3')   
s3_client.download_file('abdul-basit-bucket-for-url','constant.py', '/tmp/constan_t.py')
sys.path.insert(1,'/tmp')
import constan_t

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%   Lambda handler function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lambda_handler(event,context):
    """        Args: 
                   event(dict,optional): contains the data for a lambda fuction to process
                   context(object): passed by AWS lambda at runtime. contains methods and 
                   properties that provides information about the inocation, function,, and run time environment
    """
    value=[]                                            #creating list for more urls data
                  
    cw=Cloudwatch_putmetric()                           #class
    for url in constan_t.URL_TO_MONITOR:                 #for loop is used to pickup multiful urs from constant.Url_to_monitor
        
         avali=calc_avalibablity(url)
         latency=calc_latency(url)
         latency=calc_latency(url)
         Dimensions=[{
                    'Name': 'basit-url',
                    'Value':url},]
                    
         cw.put_matrics(constan_t.Namespace,constan_t.matric_name_avalibality,Dimensions,avali)    #Avalibality value pass to class
         cw.put_matrics(constan_t.Namespace,constan_t.matric_name_latancy,Dimensions,latency)       #Avalibality value pass to class
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


