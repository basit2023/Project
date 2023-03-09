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
    aws_s3_deployment as s3deploy_
)
from constructs import Construct

class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #Hello_lambda=self.create_lambda_function('AbdulBasit','./resource','Helloword.lambda_handler')
        
        
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the WEB Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        WebHelthLambda=self.create_lambda_function('basit_WebHealthLambda','./resource','WebHealthLambda.lambda_handler')
        WebHelthLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  S3 Bucket function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        bucket=aws_s3_.Bucket(self,"abdul-basit-bucket-for-url",bucket_name='abdul-basit-bucket-for-url',
                                                                public_read_access=True,removal_policy=RemovalPolicy.DESTROY,
                                                                auto_delete_objects=True)                                          #creating bucket in s3
        grant = bucket.grant_public_access()    #access
        bucket.apply_removal_policy(RemovalPolicy.DESTROY)
                                                                                                      #uploading file to that bucket
        s3deploy_.BucketDeployment(self,'s3_resource', sources=[s3deploy_.Source.asset('./resource',exclude =['**', '!constant.py'])],
                                                                                         
                                                                                          destination_bucket=bucket)
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/Bucket.html
        bucket=aws_s3_.Bucket(self,'abdul-basit-bucket-for-url')       #creating bucket in s3
        #uploading file to that bucket
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment.html
        s3deploy_.BucketDeployment(self,'s3_resource', 
                    #sources (Sequence[ISource]) – The sources from which to deploy the contents of this bucket.
                    sources=[s3deploy_.Source.asset('./resource')],
                    #destination_bucket (IBucket) – The S3 bucket to sync the contents of the zip file to.
                    destination_bucket=bucket)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   cron job with Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        #Schedule for scheduled event rules.
        #rate : Construct a schedule from an interval and a time unit.
        Lambda_schedule=events_.Schedule.rate(Duration.minutes(1))           #generating event after every minutes
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events_targets/LambdaFunction.html
        #Use an AWS Lambda function as an event rule target.
        Lambda_target=target_.LambdaFunction(WebHelthLambda)                 #here the event will target the lambda function
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Rule.html
        #Defines an EventBridge Rule in this stack.
        Rule=events_.Rule(self, 'Lambda_function_invocation',
            #description (Optional[str]) – A description of the rule’s purpose.
            description='periodic lambda',
            #schedule (Optional[Schedule]) – The schedule or rate (frequency) that determines when EventBridge runs the rule. 
            schedule=Lambda_schedule,
            #targets (Optional[Sequence[IRuleTarget]]) – Targets to invoke when this rule matches an event.
            targets=[Lambda_target])
            
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   ccreate a function and pass parameter    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_lambda_function(self, id_, asset, lambda_handler):             #create a function and pass different parameter
        return lambda_.Function(self, id_,
               #code (Code) – The source code of your Lambda function. 
               code=lambda_.Code.from_asset(asset),
               #runtime (Runtime) – The runtime environment for the Lambda function that you are uploading. 
               runtime=lambda_.Runtime.PYTHON_3_6,
               #handler (str) – The name of the method within your code that Lambda calls to execute your function.
               handler=lambda_handler)
