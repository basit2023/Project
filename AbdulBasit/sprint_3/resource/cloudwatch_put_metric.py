import boto3
import datetime
class Cloudwatch_putmetric:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    def put_matrics(self,Namespace,MetricName,Dimentions,value):
        """
         This function calculate the merics for the avalibality and latency
         Arg:
            MetricName: this give the name of the metric
            Dimentions: dimentions to this metric
            value:value to that metric
        """
        response = self.client.put_metric_data(
             Namespace=Namespace,
            MetricData=[
              {
               'MetricName':MetricName ,
               'Dimensions':Dimentions,
                'Timestamp': datetime.datetime.now(),
               'Value': value
            
             },
            ]
          )
        return response