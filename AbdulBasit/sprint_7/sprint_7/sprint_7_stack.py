from aws_cdk import (
                   Stack,
                   RemovalPolicy,
                   Duration,
                  # aws_sqs as sqs,
                  aws_lambda as lambda_,
                  aws_events as events_,
                  aws_events_targets as target_,
                  aws_cloudwatch as cloudwatch_,
                  aws_iam as aws_iam_,
                  aws_dynamodb as dynamodb,
                  aws_lambda_event_sources as sources,
                  aws_apigateway as apigateway_,
                  aws_sqs as sqs
)
from constructs import Construct

class Sprint7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sqs/Queue.html
        queue = sqs.Queue(self, "Abdulbasit SQS", 
                 #content_based_deduplication (Optional[bool]) – Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message.
                 content_based_deduplication=True,
                 #queue_name (Optional[str]) – A name for the queue. If specified and this is a FIFO queue, must end in the string ‘.fifo’. Default: CloudFormation-generated name
                 queue_name="Basitsqs.fifo")

        db_lambda_role = self.create_db_lambda_role()
        
        cron_lambda=self.create_lambda_function('basit_cron_lambda','./workflows','cron_lambda.lambda_handler',db_lambda_role)
        cron_lambda.add_environment('queue_name',queue.queue_name)
        
        
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   cron job with Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        Lambda_schedule=events_.Schedule.rate(Duration.minutes(1))           #generating event after every minutes
        Lambda_target=target_.LambdaFunction(cron_lambda)                 #here the event will target the lambda function
        Rule=events_.Rule(self, 'Lambda_function_invocation',
                                 description='periodic lambda',
                                 schedule=Lambda_schedule,
                                 targets=[Lambda_target])
                                 
                                 
        
        
        lambda_action=self.create_lambda_function('basit_Lambda','./resource','lambda_action.lambda_handler',db_lambda_role)
        eventSource = sources.SqsEventSource(queue)
        lambda_action.add_event_source(eventSource)
        
        
        
        
        
        
        
        table=self.create_table1(id='abdulbasittable', key=dynamodb.Attribute(name="link", type=dynamodb.AttributeType.STRING))
        
        lambda_for_api=self.create_lambda_function('basit_APILambda','./resource','API_lambda.lambda_handler',db_lambda_role)
        lambda_for_api.grant_invoke( aws_iam_.ServicePrincipal("apigateway.amazonaws.com"))   
        lambda_for_api.add_environment('table_name',table.table_name)
        table.grant_full_access(lambda_for_api)
        
        lambda_for_api.add_environment('table_name',table.table_name)
        lambda_for_api.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        """
          APIs are defined as a hierarchy of resources and methods. addResource and addMethod 
          can be used to build this hierarchy. The root resource is api.root.
           
          REST API that routes all requests to the specified AWS Lambda function
        """
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html
        api = apigateway_.LambdaRestApi(self, "AbdulBasitAPI",handler=lambda_for_api) #REST API
        items = api.root.add_resource("items")
        items.add_method("GET") # GET items
        items.add_method("PUT") # PUT items
        items.add_method("DELETE") # PUT items
        items.add_method("POST")  #update items
        
        
        
        
    def create_lambda_function(self, id_, asset, lambda_handler,rule):             #create a function and pass different parameter
        """
         Arg;
          id (str): id for function
          runtime (Runtime): The runtime environment for the Lambda function that you are uploading
          role (Optional[IRole]) – Lambda execution role.This is the role that will be assumed 
          by the function upon execution.
          handler (str) – The name of the method within your code that Lambda calls to execute your function.
        
        """
        return lambda_.Function(self, id_,
                                      code=lambda_.Code.from_asset(asset),
                                      runtime=lambda_.Runtime.PYTHON_3_6,
                                      handler=lambda_handler,
                                      timeout=Duration.seconds(30),
                                      role=rule)
    def create_table1(self,id,key):
        return dynamodb.Table(self,id,
        partition_key=key)
        
        
    def create_db_lambda_role(self):
        lambdaRole = aws_iam_.Role(self, "lambda-role-db",
                        assumed_by = aws_iam_.ServicePrincipal('lambda.amazonaws.com'),
                        managed_policies=[
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonSQSFullAccess')
                            
                        ])
        return lambdaRole
