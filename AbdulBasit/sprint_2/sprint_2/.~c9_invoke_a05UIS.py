from aws_cdk import (
    # Duration,
                   Stack,
                   RemovalPolicy,
                   Duration,
    
                  # aws_sqs as sqs,
                  aws_lambda as lambda_,
                  aws_events as events_,
                  aws_events_targets as target_,
                  aws_s3 as aws_s3_,
                  aws_s3_deployment as s3deploy_,
                  aws_cloudwatch as cloudwatch_,
                  aws_iam as aws_iam_,
                  )
from constructs import Construct
resource import constant as constant
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #Hello_lambda=self.create_lambda_function('AbdulBasit','./resource','Helloword.lambda_handler')
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        rule=self.create_lambda_rule()
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the WEB Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        WebHelthLambda=self.create_lambda_function('basit_WebHealthLambda','./resource','WebHealthLambda.lambda_handler',rule)
        WebHelthLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  S3 Bucket function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        bucket=aws_s3_.Bucket(self,'abdul-basit-bucket-for-url',bucket_name='abdul-basit-bucket-for-url',public_read_access=True,removal_policy=RemovalPolicy.DESTROY,auto_delete_objects=True)       #creating bucket in s3
        #uploading file to that bucket
        s3deploy_.BucketDeployment(self,'s3_resource', sources=[s3deploy_.Source.asset('./resource')],exclude=["*"],include=["constant.py"],destination_bucket=bucket,)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   cron job with Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        Lambda_schedule=events_.Schedule.rate(Duration.minutes(1))           #generating event after every minutes
        Lambda_target=target_.LambdaFunction(WebHelthLambda)                 #here the event will target the lambda function
        Rule=events_.Rule(self, 'Lambda_function_invocation',
            description='periodic lambda',schedule=Lambda_schedule,
            targets=[Lambda_target])
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       # s3_client=boto3.client('s3')   
       # s3_client.download_file('abdul-basit-bucket-for-url','constant.py', '/tmp/constan_t.py')
        #import constan_t
        dimensions={'AbdulBasit :url':constant.URL_TO_MONITOR}
        latency_alaram=self.create_latency_alaram(constant.URL_TO_MONITOR,dimensions)
        
        
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   ccreate a function and pass parameter    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_lambda_function(self, id_, asset, lambda_handler,rule):             #create a function and pass different parameter
        return lambda_.Function(self, id_,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_6,
        handler=lambda_handler,timeout=Duration.seconds(30), role=rule)
   
    
    def create_lambda_rule(self):
        """
            This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have.
             Args:
                  constructor
             Returns:
             Rules for lambda function created by aws_iam role. it creates two rule
        
            1)AWSLambdaBasicExecutionRole
            2)CloudWatchFullAccess
        """
        lambda_rule = aws_iam_.Role(self, "Role",                     
            assumed_by=aws_iam_.ServicePrincipal("lambda.amazonaws.com"),
            description="showing logs on cloudwhatch",
            managed_policies=[aws_iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'), #AWSLambdaBasicExecutionRole grants permissions to upload logs to CloudWatch.
            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')])
            
        return lambda_rule
        
###############################################################################################
##########################################################################################
###############################################################################################
    def create_latency_alaram(self,url,dimensions):
        """
        Created a cloudwatch Alarm that activates when avalibality is zero
        some of the parameter of the alaram cloudwatch
                id(str): contanins a string of url and metric avalibality
                metric(Iffunction):cloudwatch metric
                alarm_name(str):name of the alarm_name
                threshold (Union[int, float]) – The value against which the specified statistic is compared.
                alarm_description (Optional[str]) – Description for the alarm
                comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching. 
                evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
                treat_missing_data (Optional[TreatMissingData]) – Sets how this alarm is to handle missing data points.
                (Specify how missing data points are treated during alarm evaluation.)

        """
        avalibality_metric = cloudwatch_.Metric(
                  namespace=constant.Namespace,
                  dimensions=dimensions,
                  metric_name=constant.matric_name_avalibality,
                  label='avalibality_metric'
              )
        return cloudwatch_.Alarm(self,
                                     'AbdulBasit'+url+ constant.matric_name_avalibality,
                                      metric=avalibality_metric,
                                      threshold=constant.Threshold_Avalibality,
                                      evaluation_periods=1,
                                      alarm_description ='Alarm will activate when web page no longer avalibal',
                                      alarm_name='AbdulBasit'+url+ constant.matric_name_avalibality,
                                      comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                      datapoints_to_alarm=1,
                                      treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
                                      )
                                
              







