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
                  aws_sns as sns_,
                  aws_cloudwatch_actions as cw_actions_,
                  aws_sns_subscriptions as subscriptions_,
                  aws_dynamodb as dynamodb
                  )
import os
from constructs import Construct
from resource import constant as constant
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #Hello_lambda=self.create_lambda_function('AbdulBasit','./resource','Helloword.lambda_handler')
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the WEB Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        rule=self.create_lambda_rule()
        WebHelthLambda=self.create_lambda_function('basit_WebHealthLambda','./resource','WebHealthLambda.lambda_handler',rule)
        WebHelthLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  S3 Bucket function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/Bucket.html
        bucket=aws_s3_.Bucket(self,"abdul-basit-bucket",
                    #bucket_name (Optional[str]) – Physical name of this bucket.
                    bucket_name='abdul-basit-bucket',
                    #public_read_access (Optional[bool]) – Grants public read access to all objects in the bucket.
                    public_read_access=True,
                    #removal_policy (Optional[RemovalPolicy]) – Policy to apply when the bucket is removed from this stack.
                    removal_policy=RemovalPolicy.DESTROY,
                    #auto_delete_objects (Optional[bool]) – Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted.
                    auto_delete_objects=True)                                          #creating bucket in s3
        
        bucket.apply_removal_policy(RemovalPolicy.DESTROY)
        #uploading file to that bucket
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/BucketDeployment.html                                                                                             #uploading file to that bucket
        s3deploy_.BucketDeployment(self,'s3_resource', 
                    #sources (Sequence[ISource]) – The sources from which to deploy the contents of this bucket.
                    
                    sources=[
                           #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/Source.html
                           ##Specifies bucket deployment source.
                           s3deploy_.Source.asset('./resource',
                                     #exclude (Optional[Sequence[str]]) – (deprecated) Glob patterns to exclude from the copy.
                                     exclude =['**', '!constant.py'])],
                    ##destination_bucket (IBucket) – The S3 bucket to sync the contents of the zip file to.                                                                 
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
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ########################## Subscription ########################
        ##################################################################################################
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        ##SNS topic is a logical access point that acts as a communication channel. when alarm trigger it will activated
        topic = sns_.Topic(self,constant.TOPIC) 
        #Subscribe some endpoint to this topic
        topic.add_subscription(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
            #when topic become active then this send a message to the user
            #Use an email address as a subscription target
            subscriptions_.EmailSubscription(constant.Email_Address))   
        ##################################################################################################
        #################### Pasing URL to the create latency alarm fuunction ###################
        ##################################################################################################
        for url in constant.URL_TO_MONITOR:
             dimensions={'basit-url':url} 
             #this function return the action of the alarm on the avalibality
             avilabality_alaram=self.create_alaram(url,dimensions,metric_name=constant.matric_name_avalibality,label='avalibality')  
             #this function return the action of the alarm on the latency
             latency_alaram=self.create_alaram(url,dimensions,metric_name=constant.matric_name_latancy,label='Latency')    
              #if the avalibality alarm triggered then they gives message to topic
             avilabality_alaram.add_alarm_action(cw_actions_.SnsAction(topic))  
             #if the avalibality alarm triggered then they gives message to topic
             latency_alaram.add_alarm_action(cw_actions_.SnsAction(topic))          
        ###################################################################################################################
        ########################### DynamoDB Table #############################################
        ################################################################################################################
        #create a DynamoDB lambda 
        dynamodb_lambda=self.create_lambda_function('AbdulBasitDynamoDBLambda','./resource','db_lambda.lambda_handler',self.create_iam_role(constant.Dynamodbpolicy))    
        dynamodb_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        topic.add_subscription(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
            #Use a Lambda function as a subscription target.
            subscriptions_.LambdaSubscription(fn=dynamodb_lambda))    #when topic become active then this lambda will invoke
        ##########################################################################################################
        ######################################### Dynamo DB table function ########################
        ###########################################################################################################
        log_table=self.create_table(constant.Table)
        log_table.grant_read_write_data(dynamodb_lambda)
        dynamodb_lambda.add_environment('table_name',log_table.table_name)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   create a Lambda function and pass parameter    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def create_lambda_function(self, id_, asset, lambda_handler,rule):             #create a function and pass different parameter
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        return lambda_.Function(self, id_,
               #code (Code) – The source code of your Lambda function. 
               code=lambda_.Code.from_asset(asset),
               #runtime (Runtime) – The runtime environment for the Lambda function that you are uploading. 
               runtime=lambda_.Runtime.PYTHON_3_6,
               #handler (str) – The name of the method within your code that Lambda calls to execute your function.
               handler=lambda_handler,
               #timeout (Optional[Duration]) – The function execution time (in seconds) after which Lambda terminates the function. 
               #Because the execution time affects cost, set this value based on the function’s expected execution time.
               timeout=Duration.seconds(30), 
               #Role. You can call addToRolePolicy to the created lambda to add statements post creation.
               role=rule)
   
    
    def create_lambda_rule(self):
    
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        #Defines an IAM role. The role is created with an assume policy document associated with the specified AWS service principal defined in serviceAssumeRole.
        ##This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have.
        lambda_rule = aws_iam_.Role(self, "Role",
               #assumed_by (IPrincipal) – The IAM principal (i.e. new ServicePrincipal('sns.amazonaws.com')) which can assume this role.
               #You can later modify the assume role policy document by accessing it via the assumeRolePolicy property.
               assumed_by=aws_iam_.ServicePrincipal("lambda.amazonaws.com"),
               #description (Optional[str]) – A description of the role.
               description="showing logs on cloudwhatch",
               #managed_policies (Optional[Sequence[IManagedPolicy]]) – A list of managed policies associated with this role.
               managed_policies=[aws_iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'), #AWSLambdaBasicExecutionRole grants permissions to upload logs to CloudWatch.
               aws_iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
               aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')])
            
        return lambda_rule
        
###############################################################################################
############################### avalibality_alaram ###################################################
###############################################################################################
    def create_alaram(self,url,dimensions,metric_name,label):
       
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        #A metric emitted by a service.
        #The metric is a combination of a metric identifier (namespace, name and dimensions) and an aggregation function (statistic, period and unit).
        avalibality_metric = cloudwatch_.Metric(
                            #metric_name (str) – Name of the metric.
                            metric_name=metric_name,
                            #namespace (str) – Namespace of the metric.
                            namespace=constant.Namespace,
                            #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                            dimensions_map=dimensions,
                            #label (Optional[str]) – Label for this metric when added to a Graph in a Dashboard.
                            label=label,
                            #statistic (Optional[str]) – What function to use for aggregating. Can be one of the following:
                            #- “Minimum” | “min” - “Maximum” | “max” - “Average” | “avg” - “Sum” | “sum”
                            statistic='Average'
                                                                   )
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        #An alarm on a CloudWatch metric.
        return cloudwatch_.Alarm(self,
                            url+ ' ' + metric_name,
                            #metric (IMetric) – The metric to add the alarm on.
                            metric=avalibality_metric,
                            #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                            threshold=constant.Threshold_Avalibality,
                            #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold.
                            evaluation_periods=1,
                            #alarm_description (Optional[str]) – Description for the alarm. 
                            alarm_description ='Alarm will activate when web page no longer avalibal',
                            #alarm_name (Optional[str]) – Name of the alarm.
                            alarm_name='AbdulBasit '+url+ ' ' +metric_name,
                            #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                            #datapoints_to_alarm (Union[int, float, None]) – The number of datapoints that must be breaching to trigger the alarm.
                            datapoints_to_alarm=1,
                            #treat_missing_data (Optional[TreatMissingData]) – Sets how this alarm is to handle missing data points.
                            treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
                                      )
                     
    
    
    #######################################################################################
    ####################### table for Dynamo DB ########################################
    #####################################################################################
    def create_table(self,t_name):
        
        try:
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html
            global_table =dynamodb.Table(self, t_name,
            #billing_mode (Optional[BillingMode]) – Specify how you are charged for read and write throughput and how you manage capacity.
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            #partition_key (Attribute) – Partition key attribute definition.
            partition_key=dynamodb.Attribute(name="MessageId", type=dynamodb.AttributeType.STRING),
            #sort_key = dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
            #removal_policy (Optional[RemovalPolicy]) – The removal policy to apply to the DynamoDB Table. 
            removal_policy=RemovalPolicy.DESTROY
            )
        
        
            
        
        except:
            
            #table_name (str) – The table’s name.
            table_name=os.getenv('table_name')
            #Creates a Table construct that represents an external table via table name.
            global_table=dynamodb.Table.from_table_name(self,id,table_name)
        return global_table
        
         
    def create_iam_role(self, policy):
        #Role for Dynamo db
        ##https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        role = aws_iam_.Role(
                        self, 
                        "Role_"+policy, 
                        assumed_by=aws_iam_.ServicePrincipal("lambda.amazonaws.com"), 
                        description="Lambda Role for"+policy)
            
        role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name(policy))
            
        return role
 




