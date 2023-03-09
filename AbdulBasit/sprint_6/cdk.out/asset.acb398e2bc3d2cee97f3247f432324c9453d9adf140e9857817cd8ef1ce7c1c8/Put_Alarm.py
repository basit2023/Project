import boto3
class Alarm():
    def __init__(self):
        self.client = boto3.client('cloudwatch')    #create a cloudwatch client as a construct.
   
    """
    put_metric_alarm(**kwargs)
                     Creates or updates an alarm and associates it with the specified metric, metric math expression, or anomaly detection model.
    ARg:
       AlarmName (string) - Name of the alarm
       MetricName (string) --The name for the metric associated with the alarm. 
       Namespace (string) -- The namespace for the metric associated specified in MetricName .
       Statistic (string) -- The statistic for the metric specified in MetricName ,
       Dimensions (list) --
                    The dimensions for the metric specified in MetricName 
                    A dimension is a name/value pair that is part of the identity of a metric.
      Period (integer) --The length, in seconds, used each time the metric specified in MetricName
                       is evaluated. Valid values are 10, 30, and any multiple of 60.
    EvaluationPeriods (integer) --The number of periods over which data is compared to the specified threshold.
    Threshold (float) --The value against which the specified statistic is compared.
    ComparisonOperator (string) --[REQUIRED]The arithmetic operation to use when comparing the specified statistic and
                                  threshold. The specified statistic value is used as the first operand.
    AlarmActions (list) --
                  The actions to execute when this alarm transitions to the ALARM state from any other state.
    """
    def put_alarms(self,AlarmName,AlarmActions,MetricName,Namespace,Statistic,Dimensions,Period,EvaluationPeriods,Threshold,ComparisonOperator):
        response=self.client.put_metric_alarm(
            
                                               AlarmName=AlarmName,
                                               AlarmActions=AlarmActions,
                                               MetricName=MetricName,
                                               Namespace=Namespace,
                                               Statistic=Statistic,
                                               Dimensions=Dimensions,
                                               Period=Period,
                                               EvaluationPeriods =EvaluationPeriods,
                                               Threshold=Threshold,
                                               ComparisonOperator=ComparisonOperator,
                                               
                                              # Metrics=Metrics,
                                               )
        return response
                                               
                                               
                                               
                                               