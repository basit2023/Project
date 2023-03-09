import boto3
class Alarm():
    def __init__(self):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
        #create a cloudwatch client as a construct.
        self.client = boto3.client('cloudwatch')    
    def put_alarms(self,AlarmName,MetricName,Namespace,Statistic,Dimensions,Period,EvaluationPeriods,Threshold,ComparisonOperator,AlarmActions):
        #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm
        #put_metric_alarm(**kwargs)
        #Creates or updates an alarm and associates it with the specified metric, metric math expression, or anomaly detection model.
        response=self.client.put_metric_alarm(
                            #AlarmName (string) - Name of the alarm
                            AlarmName=AlarmName,
                            #MetricName (string) --The name for the metric associated with the alarm.
                            MetricName=MetricName,
                            #Namespace (string) -- The namespace for the metric associated specified in MetricName .
                            Namespace=Namespace,
                            #Statistic (string) -- The statistic for the metric specified in MetricName ,
                            Statistic=Statistic,
                            # Dimensions (list) --
                            #The dimensions for the metric specified in MetricName 
                            #A dimension is a name/value pair that is part of the identity of a metric.
                            Dimensions=Dimensions,
                            #Period (integer) --The length, in seconds, used each time the metric specified in MetricName
                            #is evaluated. Valid values are 10, 30, and any multiple of 60.
                            Period=Period,
                            #EvaluationPeriods (integer) --The number of periods over which data is compared to the specified threshold.
                            EvaluationPeriods =EvaluationPeriods,
                            #Threshold (float) --The value against which the specified statistic is compared.
                            Threshold=Threshold,
                            #ComparisonOperator (string) --[REQUIRED]The arithmetic operation to use when comparing the specified statistic and
                            #threshold. The specified statistic value is used as the first operand.
                            ComparisonOperator=ComparisonOperator,
                            # AlarmActions (list) --The actions to execute when this alarm transitions to the ALARM state from any other state.
                            AlarmActions=AlarmActions
                            # Metrics=Metrics,
                                               )
        return response
                                               
                                               
                                               
                                               