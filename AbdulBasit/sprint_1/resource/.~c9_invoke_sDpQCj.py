import urllib3                                                #these two are the builtin functions
import datetime
from constant import 
def lambda_handler(event,context):
    value=dict()                                               #create a dictionary to give the value for the respective keys
    avali=calc_avalibablity()
    latency=calc_latency()
    value.update({"avalibablity": avali, "latency": latency})   #put value into dict
    
def calc_avalibablity():                                        #this function is created for avalibality of the resorce
    http = urllib3.PoolManager()                                #if the resource is present then they will give the output 1.1 otherwise 0.0
    request = http.request('GET', URL_TO_MONITOR)   
    if request.status==200:
        return 1.0
    else:
        return 0.0
def calc_latency():                                             #this function will calculate the latency for a specific website
    http = urllib3.PoolManager()
    start = datetime.datetime.now()                             #noted time just before the runing url
    request = http.request('GET', URL_TO_MONITOR)               #url will run form this line
    end = datetime.datetime.now()                               #noted time just after the url responding
    diff = end - start                                          #time different between them
    return round(diff.microseconds / 1000)                      #rounding of the time
