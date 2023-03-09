import boto3
class Alarm():
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    def put_alarms(self,AlarmName,MetricName,Namespace,Statistic,Dimensions,Period,EvaluationPeriods,Threshold,ComparisonOperator,AlarmActions):
        response=self.client.put_metric_alarm(
            
                                               AlarmName=AlarmName,
                                               MetricName=MetricName,
                                               Namespace=Namespace,
                                               Statistic=Statistic,
                                               Dimensions=Dimensions,
                                               Period=Period,
                                               EvaluationPeriods =EvaluationPeriods,
                                               Threshold=Threshold,
                                               ComparisonOperator=ComparisonOperator,
                                               AlarmActions=AlarmActions
                                              # Metrics=Metrics,
                                               )
        return response
                                               
                                               
                                               
                                               