import boto3
import datetime
class Cloudwatch_putmetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    def put_matrics(self,Namespace,MetricName,Dimentions,value):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data
        #This function calculate the merics for the avalibality and latency
        response = self.client.put_metric_data(
            #The namespace for the metric data.
            Namespace=Namespace,
            #The data for the metric.
            MetricData=[
              {
                #MetricName: this give the name of the metric
                'MetricName':MetricName ,
                #Dimentions: dimentions to this metric
                'Dimensions':Dimentions,
                #time of the system
                'Timestamp': datetime.datetime.now(),
                #value:value to that metric
                'Value': value
            
             },
            ]
          )
        return response
