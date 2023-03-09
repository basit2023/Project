import urllib3                                                #these two are the builtin functions
import datetime
import constant as constant
import boto3
import sys
Access_key='AKIAUTEXLE6CE2J7TL6G'
Secret_key='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'

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%   S3 bucket download    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
     These line will download the file from s3 bucket and will store it to 
     local path (download_file)
"""
s3_client=boto3.client('s3')   
s3_client.download_file('abdul-basit-bucket-for-url','constant.py', '/tmp/constan_t.py')
sys.path.insert(1,'/tmp')
import constan_t

    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%   Lambda handler function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lambda_handler(event,context):
    value=[]                                            #creating list for more urls data
    for i in constan_t.URL_TO_MONITOR:                   #for loop is used to pickup multiful urs from constant.Url_to_monitor
        avali=calc_avalibablity(i)
        latency=calc_latency(i)
        value.append({"Avalibality":avali,"latency":latency})                  #append value to list
    return value
#####################################################################################
#%%%%%%%%%%%%%%%   Avalibality Calculation     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#####################################################################################
    
def calc_avalibablity(url):                         #this function is created for avalibality of the resorce
    http = urllib3.PoolManager()                    #if the resource is present then they will give the output 1.1 otherwise 0.0
    request = http.request('GET', url)   
    if request.status==200:
        return 1.0
    else:
        return 0.0

#####################################################################################
#%%%%%%%%%%%%%%%   Latency calculation     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#####################################################################################

def calc_latency(url):                          #this function will calculate the latency for a specific website
    http = urllib3.PoolManager()
    start = datetime.datetime.now()             #noted time just before the runing url
    request = http.request('GET', url)          #url will run form this line
    end = datetime.datetime.now()               #noted time just after the url responding
    diff = end - start                          #time different between them
    return round(diff.microseconds / 1000)      #rounding of the time
