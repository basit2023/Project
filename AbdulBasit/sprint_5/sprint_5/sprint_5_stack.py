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
                  aws_dynamodb as dynamodb,
                  aws_codedeploy as codedeploy_,
                  aws_lambda_event_sources as sources,
                  aws_s3_notifications as s3n,
                  aws_s3 as s3_,
                  aws_apigateway as apigateway_
                  )
import os
import boto3
import logging
from botocore.exceptions import ClientError
import json
import aws_cdk as cdk
from constructs import Construct
from urls_for_bucket import url_for_bucket
from resource import constant as constant
import boto3
#from dow_d_s3 import bucket3_class
class Sprint5Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #Hello_lambda=self.create_lambda_function('AbdulBasit','./resource','Helloword.lambda_handler')
        
        
        
#       #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#       #%%%%%%%%%%%%%%%   Function for the WEB Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#       #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        rule=self.create_lambda_rule(constant.CW_Access, constant.A_S3_Access, constant.AMZ_Access, constant.AWSLambdaBasicExecutionRole)
        WebHelthLambda=self.create_lambda_function('basit_WebHealthLambda','./resource','WebHealthLambda.lambda_handler',rule)
        WebHelthLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   cron job for Web Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
        #%%%%%%%%%%%%%%%  S3 Bucket function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/Bucket.html
        bucket=aws_s3_.Bucket(self,"abdul-basit-bucket",
                    #public_read_access (Optional[bool]) – Grants public read access to all objects in the bucket.
                    public_read_access=True,
                    #removal_policy (Optional[RemovalPolicy]) – Policy to apply when the bucket is removed from this stack.
                    removal_policy=RemovalPolicy.DESTROY,
                    #auto_delete_objects (Optional[bool]) – Whether all objects should be automatically deleted when the bucket is removed 
                    #from the stack or when the stack is deleted.
                    auto_delete_objects=True)                                          #creating bucket in s3
        
        bucket.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        
            
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  Lambda to read data from s3 and store to DB table    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #call the lambda function to write logs into the Dynamo DB table
        #i have subscribed this lambda function to the topic as aendpoint
        db_lambda_role = self.create_db_lambda_role()
        table_lambda=self.create_lambda_function('Table_DynamoDB_Lambda','./S3_trigger_lambda',
                                                'lambda_Db_tabal.lambda_handler',
                                                db_lambda_role)    
        table_lambda.add_environment('bucket',bucket.bucket_name)
        

        ##########################################################################################################
        ######################################### table for urls ########################
        ###########################################################################################################
        table=self.create_table1(id='abdulbasittable', key=dynamodb.Attribute(name="link", type=dynamodb.AttributeType.STRING))
        table.grant_full_access(table_lambda)
        table_lambda.add_environment('table_name',table.table_name)
        table_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        

            
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  triger lambda from s3 bucket  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

 
        # Use S3 bucket notifications as an event source for AWS Lambda.
        table_lambda.add_event_source(sources.S3EventSource(
                          #bucket (Bucket) –
                          bucket,
                          #events (Sequence[EventType]) – The s3 event types that will trigger the notification.
                          events=[s3_.EventType.OBJECT_CREATED],
                          #filters (Optional[Sequence[NotificationKeyFilter]]) – S3 object key filter rules to 
                          #determine which objects trigger this event. Each filter must include a prefix and/or
                          #suffix that will be matched against the s3 object key.
                          filters=[s3_.NotificationKeyFilter(suffix=".json")]))

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/BucketDeployment.html  
        #uploading file to that bucket
        s3deploy_.BucketDeployment(self,'s3_resource', 
                    #sources (Sequence[ISource]) – The sources from which to deploy the contents of this bucket.
                    
                    sources=[
                           #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/Source.html
                           ##Specifies bucket deployment source.
                           s3deploy_.Source.asset('./urls_for_bucket',
                                     #exclude (Optional[Sequence[str]]) – (deprecated) Glob patterns to exclude from the copy.
                                     exclude =['**', '!urls_for_bucket.json'])],
                    ##destination_bucket (IBucket) – The S3 bucket to sync the contents of the zip file to.                                                                 
                    destination_bucket=bucket)     
        
        
        
        #****************************************************************************************************
        #*************************** Lambda for APL ***********************************
        #***************************************************************************************************
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/README.html
        lambda_for_api=self.create_lambda_function('basit_APILambda','./API_lambda','API_lambda.lambda_handler',db_lambda_role)
        lambda_for_api.grant_invoke( aws_iam_.ServicePrincipal("apigateway.amazonaws.com"))   
        lambda_for_api.add_environment('table_name',table.table_name)
        table.grant_full_access(lambda_for_api)
        table.grant_full_access(WebHelthLambda)
        WebHelthLambda.add_environment('table_name',table.table_name)
        
        #APIs are defined as a hierarchy of resources and methods. addResource and addMethod 
        #can be used to build this hierarchy. The root resource is api.root.
        #REST API that routes all requests to the specified AWS Lambda function
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        api = apigateway_.LambdaRestApi(self, "AbdulBasitAPI",handler=lambda_for_api) #REST API
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource
        #root:Represents the root resource of this API endpoint
        #add_resource: Defines a new child resource where this resource is the parent.
        items = api.root.add_resource("items")
        items.add_method("GET") # GET items
        items.add_method("PUT") # PUT items
        items.add_method("DELETE") # PUT items
        items.add_method("POST")  #update items






    
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
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        #The ARN of the topic.
        sns_topic_arn=topic.topic_arn
        #add sns_topic to webhelthlambda environment
        WebHelthLambda.add_environment('sns_topic_arn',sns_topic_arn)
       
       
       
       
       
       
        ##################################################################################################
        #################### Passing URL to create metric and alarm action ###################
        ##################################################################################################
        for url in constant.URL_TO_MONITOR:
             dimensions={'basit-urls':url}                               
             avilabality_alaram=self.create_metric_for_alaram(name=constant.matric_name_avalibality, 
                                                                 url=url, 
                                                                 namespace=constant.Namespace,
                                                                 dimensions_map=dimensions,
                                                                 operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
                                                                 period=constant.PERIOD, 
                                                                 threshold=constant.Threshold_Avalibality,
                                                                 treat_missing_data=cloudwatch_.TreatMissingData.BREACHING)      #this function return the action of the alarm on the avalibality
             latency_alaram=self.create_metric_for_alaram(name=constant.matric_name_latancy,
                                                                 url=url, 
                                                                 namespace=constant.Namespace,
                                                                 dimensions_map=dimensions,
                                                                 operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
                                                                 period=constant.PERIOD, 
                                                                 threshold=constant.Threshold_latency,
                                                                 treat_missing_data=cloudwatch_.TreatMissingData.BREACHING)              #this function return the action of the alarm on the latency
             
             #when the avalibality alarm triggered then they give message to topic
             avilabality_alaram.add_alarm_action(cw_actions_.SnsAction(topic))  
             #when the latency alarm triggered then they give message to topic
             latency_alaram.add_alarm_action(cw_actions_.SnsAction(topic))  




        ###################################################################################################################
        ########################### DynamoDB Lambda function for storing alram logs ####################
        ###################################################################################################################
        #called the lambda function to write logs into the Dynamo DB table
        #i subscribe this lambda function to the topic as aendpoint
        dynamodb_lambda=self.create_lambda_function('AbdulBasitDynamoDBLambda','./Log_store_lambda',
                                                    'db_lambda.lambda_handler',
                                                     self.create_iam_role(constant.AMZ_Access, constant.Dynamodbpolicy,constant.AWSLambdaBasicExecutionRole))    
        dynamodb_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        topic.add_subscription(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/LambdaSubscription.html
            #Use a Lambda function as a subscription target.
            ##when topic become active then this lambda will invoke
            subscriptions_.LambdaSubscription(fn=dynamodb_lambda))  



        ##########################################################################################################
        ######################################### Dynamo DB table function  ########################
        ###########################################################################################################
        log_table=self.create_table(constant.Table)
        log_table.grant_read_write_data(dynamodb_lambda)
        dynamodb_lambda.add_environment('table_name',log_table.table_name)
        
        
        
 #####################################################################################################################
#***************************** Failur Matrics and Alrams for DynamoDb lambda Duration***********************
#####################################################################################################################
       
        #Lambda Metric for Duration
        #These lines will return the metric for the Duration
        faliure_metric = cloudwatch_.Metric(
                            #namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
                            namespace = 'AWS/Lambda',
                            #metric_name (str) – Name of the metric, here it should be from the AwS special names
                            metric_name = 'Duration',
                            #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                            dimensions_map = {"FunctioName": dynamodb_lambda.function_name,

                                            })
       
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        # Alarm for failure metric
        faliure_alarm = cloudwatch_.Alarm(self, 
                        "alarm_for_faliure_metric_1",
                        #metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
                        #resources, or you can construct custom Metric objects by instantiating one.
                        metric = faliure_metric,
                        #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                        threshold=3500,
                        #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
                        evaluation_periods=1,
                        #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
                                                )
                                                
                                                
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        #Use an SNS topic as an alarm action.
        faliure_alarm.add_alarm_action(cw_actions_.SnsAction(topic))  
        faliure_alarm.apply_removal_policy(RemovalPolicy.DESTROY)
   
############################################################################################################################
#***************************** Failur Matrics and Alrams for DynamoDB lambda Erore ***********************
############################################################################################################################
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        #Lambda Metric for Error
        #These lines will return the metric for the Error
        faliure_2_metric = cloudwatch_.Metric(
                        #namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
                        namespace = 'AWS/Lambda',
                        #metric_name (str) – Name of the metric, here it should be from the AwS special names
                        metric_name = 'Errors',
                        #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                        dimensions_map = {"FunctioName": dynamodb_lambda.function_name,

                                            })

        # Alarm for faliure metric  2

        faliure_2_alarm = cloudwatch_.Alarm(self, "alarm_for_faliure_metric_2",
                        #metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
                        #resources, or you can construct custom Metric objects by instantiating one.
                        metric = faliure_2_metric,
                        #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                        threshold=4000,
                        #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
                        evaluation_periods=1,
                        #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
                                                )  
         #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        #Use an SNS topic as an alarm action.
        faliure_2_alarm.add_alarm_action(cw_actions_.SnsAction(topic))  
        faliure_2_alarm.apply_removal_policy(RemovalPolicy.DESTROY)        

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html
        #Alias is pointed to particaul version of lambda fnction
        alias = lambda_.Alias(self, 
                        "Lambda_Alias",
                        #alias_name (str) – Name of this alias
                        alias_name = "current",
                        #version (IVersion) – Function version this alias refers to. Use lambda.currentVersion to reference a version with your latest changes
                        version =dynamodb_lambda.current_version
                        ) 
     
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, 
                        #id (str) – id for the deployment_group
                        "WebHealthDeployment",
                        #alias (Alias) – Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.
                        alias= alias,
                        #deployment_config (Optional[ILambdaDeploymentConfig]) – The Deployment Configuration this Deployment Group uses.
                        #At means this they will transfer the linear triffic to new version lambda.
                        deployment_config= codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                        #alarms (Optional[Sequence[IAlarm]]) – The CloudWatch alarms associated with this Deployment Group. 
                        #CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger                                     
                        alarms = [faliure_alarm,faliure_2_alarm],
                                                )    

 
#********************************************************************************************************************
#********************* Failur Matrics and Alrams for webHealth lambda Duration **********************************
#********************************************************************************************************************
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        #Lambda Metric for Duration
        #These lines will access to the Duration
        faliure_metric_wh = cloudwatch_.Metric(
                            #namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
                            namespace = 'AWS/Lambda',
                            #metric_name (str) – Name of the metric, here it should be from the AwS special names
                            metric_name = 'Duration',
                            #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                            dimensions_map = {"FunctioName": WebHelthLambda.function_name,

                                            })

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        # Alarm for failure metric
        faliure_alarm_wh = cloudwatch_.Alarm(self, 
                        "alarm_for_faliure_metric_1_wh",
                        #metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
                        #resources, or you can construct custom Metric objects by instantiating one.
                        metric = faliure_metric_wh,
                        #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                        threshold=4000,
                        #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
                        evaluation_periods=1,
                        #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
                                                )
         
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        #Use an SNS topic as an alarm action.
        faliure_alarm_wh.add_alarm_action(cw_actions_.SnsAction(topic))  
        faliure_alarm_wh.apply_removal_policy(RemovalPolicy.DESTROY)
#********************************************************************************************************************
#********************* Failur Matrics and Alrams for webHealth lambda Erore **********************************
#********************************************************************************************************************
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        #Lambda Metric for Error
        #These lines will return the metric for the Error
        faliure_2_metric_wh = cloudwatch_.Metric(
                        #namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
                        namespace = 'AWS/Lambda',
                        #metric_name (str) – Name of the metric, here it should be from the AwS special names
                        metric_name = 'Errors',
                        #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                        dimensions_map = {"FunctioName": WebHelthLambda.function_name,

                                            })

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        # Alarm for failure metric
        faliure_2_alarm_wh = cloudwatch_.Alarm(self, 
                        "alarm_for_faliure_metric_2_wh",
                        #metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
                        #resources, or you can construct custom Metric objects by instantiating one.
                        metric = faliure_metric,
                        #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                        threshold=3500,
                        #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
                        evaluation_periods=1,
                        #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                        comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
                                                )
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        #Use an SNS topic as an alarm action.
        faliure_2_alarm_wh.add_alarm_action(cw_actions_.SnsAction(topic))  
        faliure_2_alarm_wh.apply_removal_policy(RemovalPolicy.DESTROY)        

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html
        #Alias is pointed to particaul version of lambda fnction
        alias_wh = lambda_.Alias(self, 
                        "Lambda_Alias_wh",
                        #alias_name (str) – Name of this alias
                        alias_name = "current",
                        #version (IVersion) – Function version this alias refers to. Use lambda.currentVersion to reference a version with your latest changes
                        version =WebHelthLambda.current_version
                        ) 

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, 
                        #id (str) – id for the deployment_group
                        "WebHealthDeployment_wh",
                        #alias (Alias) – Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.
                        alias= alias_wh,
                        #deployment_config (Optional[ILambdaDeploymentConfig]) – The Deployment Configuration this Deployment Group uses.
                        #At means this they will transfer the linear triffic to new version lambda.
                        deployment_config= codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                        #alarms (Optional[Sequence[IAlarm]]) – The CloudWatch alarms associated with this Deployment Group. 
                        #CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger                                     
                        alarms = [faliure_alarm_wh,faliure_2_alarm_wh],
                                                )   
   
    
    
    
    
    

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
                                      
                                      
                                      
                                      
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%   Lambda role    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
    def create_lambda_rule(self,CW_Access,A_S3_Access,AMZ_Access,AWSLambdaBasicExecutionRole):
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        #Defines an IAM role. The role is created with an assume policy document associated with the specified AWS service principal defined in serviceAssumeRole.
        ##This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have.
        lambda_rule = aws_iam_.Role(self, "Role",                     
                #assumed_by (IPrincipal) – The IAM principal (i.e. new ServicePrincipal('sns.amazonaws.com')) which can assume this role.
                #You can later modify the assume role policy document by accessing it via the assumeRolePolicy property.                    
                assumed_by=aws_iam_.ServicePrincipal(AMZ_Access),
                #description (Optional[str]) – A description of the role.                   
                description="showing logs on cloudwhatch",
                #managed_policies (Optional[Sequence[IManagedPolicy]]) – A list of managed policies associated with this role.
                managed_policies=[aws_iam_.ManagedPolicy.from_aws_managed_policy_name(AWSLambdaBasicExecutionRole), #AWSLambdaBasicExecutionRole grants permissions to upload logs to CloudWatch.
                aws_iam_.ManagedPolicy.from_aws_managed_policy_name(CW_Access),
                aws_iam_.ManagedPolicy.from_aws_managed_policy_name(A_S3_Access),
                aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')])
            
        return lambda_rule   
        
        
        
        
        
        
        

###############################################################################################
######################## avalibality and latency metrics and alarams ##########################
###############################################################################################
    def create_metric_for_alaram(self, name, url, namespace, dimensions_map,operator, period, threshold, treat_missing_data):
    
        #Created a cloudwatch Alarm that activates when avalibality is zero
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        #A metric emitted by a service.
        #The metric is a combination of a metric identifier (namespace, name and dimensions) and an aggregation function (statistic, period and unit).
        metric = cloudwatch_.Metric(
                                    #metric_name (str) – Name of the metric.
                                    metric_name=name,
                                    #namespace (str) – Namespace of the metric.
                                    namespace=namespace,
                                    #dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
                                    dimensions_map=dimensions_map,
                                    #period (Optional[Duration]) – The period over which the specified statistic is applied.
                                    period=Duration.minutes(period)
                                                                  )
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        #An alarm on a CloudWatch metric.                                                          
        return cloudwatch_.Alarm(self,
                                      id=url+ ' ' + name,
                                      #metric (IMetric) – The metric to add the alarm on.
                                      metric=metric,
                                       #comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
                                      comparison_operator=operator,
                                       #evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold.
                                      evaluation_periods = period,
                                      #threshold (Union[int, float]) – The value against which the specified statistic is compared.
                                      threshold=threshold,
                                      #treat_missing_data (Optional[TreatMissingData]) – Sets how this alarm is to handle missing data points.
                                      treat_missing_data=treat_missing_data
                                      )                                                              
    
   
   
   
   
    
        
    #######################################################################################
    ####################### table for Dynamo DB ########################################
    #####################################################################################
    def create_table(self,t_name):
        
        try:
            ##https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html     
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
        
        
        
        
        
        
        
        
        
        
    #######################################################################################
    ####################### lambdas rules ########################################
    #####################################################################################        
        #this policy is just for the access to DynamoDB table'
         
    def create_iam_role(self, AMZ_Access,policy,AWSLambdaBasicExecutionRole):
        
        #Creates an IAM Role and add polices.
        #Role for Dynamo db
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        #Defines an IAM role. The role is created with an assume policy document associated with the specified AWS service principal defined in serviceAssumeRole.
        ##This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have.
        role = aws_iam_.Role(
            self, 
            "Role_"+policy, 
            #assumed_by (IPrincipal) – The IAM principal (i.e. new ServicePrincipal('sns.amazonaws.com')) which can assume this role.
            #You can later modify the assume role policy document by accessing it via the assumeRolePolicy property.
            assumed_by=aws_iam_.ServicePrincipal(AMZ_Access), 
            #description (Optional[str]) – A description of the role.
            description="Lambda Role for"+policy)
            
        role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name(AWSLambdaBasicExecutionRole))
        role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name(policy))
            
        return role
        
        
    def create_db_lambda_role(self):
        #Creates an IAM Role and add polices.
        #Role for Dynamo db
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        #Defines an IAM role. The role is created with an assume policy document associated with the specified AWS service principal defined in serviceAssumeRole.
        ##This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have.
        lambdaRole = aws_iam_.Role(self, "lambda-role-db",
                        #assumed_by (IPrincipal) – The IAM principal (i.e. new ServicePrincipal('sns.amazonaws.com')) which can assume this role.
                        #You can later modify the assume role policy document by accessing it via the assumeRolePolicy property.
                        assumed_by = aws_iam_.ServicePrincipal('lambda.amazonaws.com'),
                         #managed_policies (Optional[Sequence[IManagedPolicy]]) – A list of managed policies associated with this role.
                        managed_policies=[
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonSNSFullAccess'),
                            aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
                            
                        ])
        return lambdaRole
        
    #######################################################################################
    ####################### table for Dynamo DB ########################################
    #####################################################################################
    def create_table1(self,id,key):
        return dynamodb.Table(self,id,
        partition_key=key)    
        
    # create bucket for json to read from py and store it into json and uploade it to s3
    # def creat_bucket(self,bucket_name):
    #     try:
    #         file_name="./urls_for_bucket/urls_for_bucket.json"
    #         with open(file_name, 'w') as outfile:
    #              json.dump(url_for_bucket.URL_TO_MONITOR,outfile)
    #         session = boto3.session.Session()
    #         current_region=session.region_name
    #         s3_client=boto3.client('s3',region_name=current_region) 
    
        
    #         s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': current_region})
    #         response = s3_client.put_object(Body=json.load(file_name),Bucket=bucket_name,key='urls_for_bucket/urls_for_bucket.json')
    #     except ClientError as e:
    #         logging.error(e)
    #         return False
    #     return True    
    