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
                  aws_codedeploy as codedeploy_
                  )
import os
import Boto3
import logging
import aws_cdk as cdk
from constructs import Construct
from resource import urls_for_bucket as urls_for_bucket
import constant as constant
class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%   Function for the Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #Hello_lambda=self.create_lambda_function('AbdulBasit','./resource','Helloword.lambda_handler')
        
        
        
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%   Function for the WEB Health Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        rule=self.create_lambda_rule(constant.CW_Access, constant.A_S3_Access, constant.AMZ_Access, constant.AWSLambdaBasicExecutionRole)
        WebHelthLambda=self.create_lambda_function('basit_WebHealthLambda','./resource','WebHealthLambda.lambda_handler',rule)
        WebHelthLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        bucket=self.c
         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       # json_lambda=self.create_lambda_function('basit_json_lambda','./resource','json_lambda.lambda_handler',rule)
       # json_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%  S3 Bucket function    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # bucket=aws_s3_.Bucket(self,"bucket-for-url",bucket_name='bucket-for-url',
        #                                                         public_read_access=True,removal_policy=RemovalPolicy.DESTROY,
        #                                                         auto_delete_objects=True)                                          #creating bucket in s3
        # grant = bucket.grant_public_access()    #access
        # bucket.apply_removal_policy(RemovalPolicy.DESTROY)
        #                                                                                               #uploading file to that bucket
        # s3deploy_.BucketDeployment(self,'s3_resource', sources=[s3deploy_.Source.asset('./resource',exclude =['**', '!urls_for_bucket.json'])],
                                                                                         
        #                                                                                   destination_bucket=bucket)
def creat_bucket():
    try:
        file_name="./urls_for_bucket/urls_for_bucket.json"
        with open(file_name, 'w') as outfile:
             json.dump(url_for_bucket.URL_TO_MONITOR,outfile)
        session = boto3.session.Session()
        current_region=session.region_name
        s3_client=boto3.client('s3',region_nam=current_region) 
    
        
        s3_client.create_bucket(Bucket='bucket-for-url', CreateBucketConfiguration={'LocationConstraint': current_region})
        response = s3_client.put_object(Body=json.load(file_name),Bucket='bucket-for-url',key='urls_for_bucket/urls_for_bucket.json')
    except ClientError as e:
        logging.error(e)
        return False
    return True
            
#         # WebHelthLambda.add_environment('bucket',bucket.bucket_name)
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%   cron job with Lambda    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         Lambda_schedule=events_.Schedule.rate(Duration.minutes(1))           #generating event after every minutes
#         Lambda_target=target_.LambdaFunction(WebHelthLambda)                 #here the event will target the lambda function
#         Rule=events_.Rule(self, 'Lambda_function_invocation',
#                                  description='periodic lambda',
#                                  schedule=Lambda_schedule,
#                                  targets=[Lambda_target])
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         ########################## Subscription ########################
#         ##################################################################################################
#         topic = sns_.Topic(self,constant.TOPIC) #SNS topic is a logical access point that acts as a communication channel. when alarm trigger it will activated
#         topic.add_subscription(subscriptions_.EmailSubscription(constant.Email_Address))   #when topic become active then this send a message to the user
#         ##################################################################################################
#         #################### Pasing URL to the create latency alarm fuunction ###################
#         ##################################################################################################
#         for url in constant.URL_TO_MONITOR:
#              #dimensions={'basit-url':url}                               
#              avilabality_alaram=self.create_metric_for_alaram(name=constant.matric_name_avalibality, 
#                                                                  url=url, 
#                                                                  namespace=constant.Namespace,
#                                                                  operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
#                                                                  period=constant.PERIOD, 
#                                                                  threshold=constant.Threshold_Avalibality,
#                                                                  topic=topic,treat_missing_data=cloudwatch_.TreatMissingData.BREACHING)      #this function return the action of the alarm on the avalibality
#              latency_alaram=self.create_metric_for_alaram(name=constant.matric_name_latancy,
#                                                                  url=url, 
#                                                                  namespace=constant.Namespace,
#                                                                  operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
#                                                                  period=constant.PERIOD, 
#                                                                  threshold=constant.Threshold_latency,
#                                                                  topic=topic,treat_missing_data=cloudwatch_.TreatMissingData.BREACHING)              #this function return the action of the alarm on the latency
#              avilabality_alaram.add_alarm_action(cw_actions_.SnsAction(topic))      #if the avalibality alarm triggered then they give message to topic
#              latency_alaram.add_alarm_action(cw_actions_.SnsAction(topic))          #if the avalibality alarm triggered then they give message to topic
#         ###################################################################################################################
#         ########################### DynamoDB Table #############################################
#         ################################################################################################################
#         #called the lambda function to write logs into the Dynamo DB table
#         #i subscribe this lambda function to the topic as aendpoint
#         dynamodb_lambda=self.create_lambda_function('AbdulBasitDynamoDBLambda','./resource',
#                                                     'db_lambda.lambda_handler',
#                                                      self.create_iam_role(constant.AMZ_Access, constant.Dynamodbpolicy,constant.AWSLambdaBasicExecutionRole))    
#         dynamodb_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
#         topic.add_subscription(subscriptions_.LambdaSubscription(fn=dynamodb_lambda))    #when topic become active then this lambda will invoke
#         ##########################################################################################################
#         ######################################### Dynamo DB table function ########################
#         ###########################################################################################################
#         """
#         wh_table = dynamodb.Table(self, "WebHealthDynamoTable",
#             table_name = constant.Table,
#             partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
#             sort_key = dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
#             removal_policy=RemovalPolicy.DESTROY
#             )
#         dynamodb_lambda.add_environment("table_name", wh_table.table_name)
#         """
#         log_table=self.create_table(constant.Table)
#         log_table.grant_read_write_data(dynamodb_lambda)
#         dynamodb_lambda.add_environment('table_name',log_table.table_name)
        
#         #************************************************************************************************
#         #***************************** Failur Matrics and Alrams ***********************
#         #************************************************************************************************
        
#         """
#         Lambda Metric for Duration
#         These lines will return the metric for the Duration
#         Arg:
#           metric_name (str) – Name of the metric, here it should be from the AwS special names 
#           namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
#           dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
#         """
#         faliure_metric = cloudwatch_.Metric(namespace = 'AWS/Lambda',
#                                             metric_name = 'Duration',
#                                             dimensions_map = {"FunctioName": dynamodb_lambda.function_name,

#                                             })
#         """
#         # Alarm for failure metric
#         Arg:
#           metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
#                               resources, or you can construct custom Metric objects by instantiating one.
#           threshold (Union[int, float]) – The value against which the specified statistic is compared.
#           evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
#           comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
#         """
#         faliure_alarm = cloudwatch_.Alarm(self, "alarm_for_faliure_metric_1",
#                                                 metric = faliure_metric,
#                                                 threshold=1,
#                                                 evaluation_periods=1,
#                                                 comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
#                                                 )
         

#         faliure_alarm.add_alarm_action(cw_actions_.SnsAction(topic))  
#         faliure_alarm.apply_removal_policy(RemovalPolicy.DESTROY)



#         """
#         Lambda Metric for Error
#         These lines will return the metric for the Duration
#         Arg:
#           metric_name (str) – Name of the metric, here it should be from the AwS special names 
#           namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
#           dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
#         """                     
#         faliure_2_metric = cloudwatch_.Metric(namespace = 'AWS/Lambda',
#                                             metric_name = 'Errors',
#                                             dimensions_map = {"FunctioName": dynamodb_lambda.function_name,

#                                             })

#         # Alarm for faliure metric  2

#         faliure_2_alarm = cloudwatch_.Alarm(self, "alarm_for_faliure_metric_2",
#                                                 metric = faliure_2_metric,
#                                                 threshold=1,
#                                                 evaluation_periods=1,
#                                                  comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD
#                                                 )  

#         faliure_2_alarm.add_alarm_action(cw_actions_.SnsAction(topic))  
#         faliure_2_alarm.apply_removal_policy(RemovalPolicy.DESTROY)        



#         """
#         # Alias is pointed to particaul version of lambda fnction
#         Arg:
#           alias_name (str) – Name of this alias.
#           version (IVersion) – Function version this alias refers to.
#           here in this function we Used lambda.addVersion() to obtain a new lambda version to refer to.
#         """
         

#         alias = lambda_.Alias(self, "Lambda_Alias", 
#                                 alias_name = "current",
#                                 version =dynamodb_lambda.current_version
#                                 ) 
#         """
#         Arg:
#           id (str) – id for the deployment_group
#           alias (Alias) – Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.
#           deployment_config (Optional[ILambdaDeploymentConfig]) – The Deployment Configuration this Deployment Group uses.
#                              At means this they will transfer the linear triffic to new version lambda.
#           alarms (Optional[Sequence[IAlarm]]) – The CloudWatch alarms associated with this Deployment Group. 
#                   CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger
#         """

#         deployment_group = codedeploy_.LambdaDeploymentGroup(self, "WebHealthDeployment",
#                                                              alias= alias,
#                                                              deployment_config= codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
                                                             
#                                                              alarms = [faliure_alarm,faliure_2_alarm],
#                                                 )    

 
#         #************************************************************************************************
#         #***************************** Failur Matrics and Alrams ***********************
#         #************************************************************************************************
        
#         """
#         Lambda Metric for Duration
#         These lines will return the metric for the Duration
#         Arg:
#           metric_name (str) – Name of the metric, here it should be from the AwS special names 
#           namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
#           dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
#         """
#         faliure_metric_wh = cloudwatch_.Metric(namespace = 'AWS/Lambda',
#                                             metric_name = 'Duration',
#                                             dimensions_map = {"FunctioName": WebHelthLambda.function_name,

#                                             })
#         """
#         # Alarm for failure metric
#         Arg:
#           metric (IMetric) – The metric to add the alarm on. Metric objects can be obtained from most
#                               resources, or you can construct custom Metric objects by instantiating one.
#           threshold (Union[int, float]) – The value against which the specified statistic is compared.
#           evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
#           comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching.
#         """
#         faliure_alarm_wh = cloudwatch_.Alarm(self, "alarm_for_faliure_metric_1_wh",
#                                                 metric = faliure_metric_wh,
                                                
#                                                 evaluation_periods=1,
#                                                 comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
#                                                 threshold=4000,
#                                                 )
         

#         faliure_alarm_wh.add_alarm_action(cw_actions_.SnsAction(topic))  
#         faliure_alarm_wh.apply_removal_policy(RemovalPolicy.DESTROY)



#         """
#         Lambda Metric for Error
#         These lines will return the metric for the Duration
#         Arg:
#           metric_name (str) – Name of the metric, here it should be from the AwS special names 
#           namespace (str) – Namespace of the metric. here it should be from the AwS special namesspace
#           dimensions_map (Optional[Mapping[str, str]]) – Dimensions of the metric.
#         """                     
#         faliure_2_metric_wh = cloudwatch_.Metric(namespace = 'AWS/Lambda',
#                                             metric_name = 'Errors',
#                                             dimensions_map = {"FunctioName": WebHelthLambda.function_name,

#                                             })

#         # Alarm for faliure metric  2

#         faliure_2_alarm_wh = cloudwatch_.Alarm(self, "alarm_for_faliure_metric_2_wh",
#                                                 metric = faliure_2_metric_wh,
                                                
#                                                 evaluation_periods=1,
#                                                  comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
#                                                  threshold=3500,
#                                                 )  

#         faliure_2_alarm_wh.add_alarm_action(cw_actions_.SnsAction(topic))  
#         faliure_2_alarm_wh.apply_removal_policy(RemovalPolicy.DESTROY)        



#         """
#         # Alias is pointed to particaul version of lambda fnction
#         Arg:
#           alias_name (str) – Name of this alias.
#           version (IVersion) – Function version this alias refers to.
#           here in this function we Used lambda.addVersion() to obtain a new lambda version to refer to.
#         """
         

#         alias_wh = lambda_.Alias(self, "Lambda_Alias_wh", 
#                                 alias_name = "current",
#                                 version =WebHelthLambda.current_version
#                                 ) 
#         """
#         Arg:
#           id (str) – id for the deployment_group
#           alias (Alias) – Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.
#           deployment_config (Optional[ILambdaDeploymentConfig]) – The Deployment Configuration this Deployment Group uses.
#                              At means this they will transfer the linear triffic to new version lambda.
#           alarms (Optional[Sequence[IAlarm]]) – The CloudWatch alarms associated with this Deployment Group. 
#                   CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger
#         """

#         deployment_group = codedeploy_.LambdaDeploymentGroup(self, "WebHealthDeployment_wh",
#                                                              alias= alias_wh,
#                                                              deployment_config= codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE,
#                                                              alarms = [faliure_alarm_wh,faliure_2_alarm_wh]
#                                                 )    

         
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%   create a Lambda function and pass parameter    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
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
                                      role=rule
                                      )
   
    
    def create_lambda_rule(self,CW_Access,A_S3_Access,AMZ_Access,AWSLambdaBasicExecutionRole):
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
                                    assumed_by=aws_iam_.ServicePrincipal(AMZ_Access),
                                    description="showing logs on cloudwhatch",
                                    managed_policies=[aws_iam_.ManagedPolicy.from_aws_managed_policy_name(AWSLambdaBasicExecutionRole), #AWSLambdaBasicExecutionRole grants permissions to upload logs to CloudWatch.
                                    aws_iam_.ManagedPolicy.from_aws_managed_policy_name(CW_Access),
                                    aws_iam_.ManagedPolicy.from_aws_managed_policy_name(A_S3_Access)])
            
        return lambda_rule
        
# ###############################################################################################
# ############################### avalibality_alaram ###################################################
# ###############################################################################################
#     def create_metric_for_alaram(self, name, url, namespace, operator, period, threshold, topic,treat_missing_data):
#         """
#         Created a cloudwatch Alarm that activates when avalibality is zero
#         some of the parameter of the alaram cloudwatch
#                 id(str): contanins a string of url and metric avalibality
#                 metric(Iffunction):cloudwatch metric
#                 alarm_name(str):name of the alarm_name
#                 threshold (Union[int, float]) – The value against which the specified statistic is compared.
#                 alarm_description (Optional[str]) – Description for the alarm
#                 comparison_operator (Optional[ComparisonOperator]) – Comparison to use to check if metric is breaching. 
#                 evaluation_periods (Union[int, float]) – The number of periods over which data is compared to the specified threshold
#                 treat_missing_data (Optional[TreatMissingData]) – Sets how this alarm is to handle missing data points.
#                 (Specify how missing data points are treated during alarm evaluation.)

#         """
#         metric = cloudwatch_.Metric(metric_name=name,
#                                                 namespace=namespace,
#                                                 dimensions_map={'basit-url':url},
#                                                 period=Duration.minutes(period)
#                                                                   )
#         return cloudwatch_.Alarm(self,
#                                       id=url+ ' ' + name,
#                                       metric=metric,
#                                       comparison_operator=operator,
#                                       evaluation_periods = period,
#                                       threshold=threshold,
                                      
                                   
#                                       treat_missing_data=treat_missing_data
#                                       )
                                                                
    
    
#     #######################################################################################
#     ####################### table for Dynamo DB ########################################
#     #####################################################################################
#     def create_table(self,t_name):
#         """
#         Arg:
#           id (str) –as a string
#           table_name (Optional[str]) – Enforces a particular physical table name. 
#           billing_mode (Optional[BillingMode]) – Specify how you are charged for read and write 
#           throughput and how you manage capacity. pay per request
#           partition_key (Attribute) – Partition key attribute definition.
#         """
#         try:
#             global_table =dynamodb.Table(self, t_name,
#             billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
#             partition_key=dynamodb.Attribute(name="MessageId", type=dynamodb.AttributeType.STRING),
#             #sort_key = dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
#             removal_policy=RemovalPolicy.DESTROY
#             )
        
        
            
        
#         except:
#             table_name=os.getenv('table_name')
#             global_table=dynamodb.Table.from_table_name(self,table_name)
#         return global_table
        
        
        
#         #this policy is just for the access to DynamoDB table'
         
#     def create_iam_role(self, AMZ_Access,policy,AWSLambdaBasicExecutionRole):
#         """
#         Creates an IAM Role and add polices.
        
#         policy (str): Name of the policy to be added
        
#         returns: IAM Role
        
#         """
#         role = aws_iam_.Role(
#             self, 
#             "Role_"+policy, 
#             assumed_by=aws_iam_.ServicePrincipal(AMZ_Access), 
#             description="Lambda Role for"+policy)
            
#         role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name(AWSLambdaBasicExecutionRole))
#         role.add_managed_policy(aws_iam_.ManagedPolicy.from_aws_managed_policy_name(policy))
            
#         return role
