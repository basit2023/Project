from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    RemovalPolicy,
    Duration,
    aws_lambda as lambda_,
    aws_s3 as s3_,
    aws_iam as aws_iam_,
    aws_s3_notifications as s3_notifications,
    aws_lambda_event_sources as sources,
    aws_s3_deployment as s3deploy_,
)
from constructs import Construct

class BasitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        rule=self.create_lambda_rule("CloudWatchFullAccess", "AmazonS3FullAccess", "lambda.amazonaws.com", 'service-role/AWSLambdaBasicExecutionRole')
        
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/Bucket.html
        bucket=s3_.Bucket(self,"abdul-basit-bucket",
                    #public_read_access (Optional[bool]) – Grants public read access to all objects in the bucket.
                    public_read_access=True,
                    #removal_policy (Optional[RemovalPolicy]) – Policy to apply when the bucket is removed from this stack.
                    removal_policy=RemovalPolicy.DESTROY,
                    #auto_delete_objects (Optional[bool]) – Whether all objects should be automatically deleted when the bucket is removed 
                    #from the stack or when the stack is deleted.
                    auto_delete_objects=True)                                          #creating bucket in s3
        
        bucket.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        
        
        
        
        lambdaaplication=self.lambdaaplication('LambdaAplication','./resource','LambdaAplication.LambdaApps',rule)
        lambdaaplication.apply_removal_policy(RemovalPolicy.DESTROY)
        lambdaaplication.add_environment('bucket',bucket.bucket_name)
         # Use S3 bucket notifications as an event source for AWS Lambda.
        # lambdaaplication.add_event_source(sources.S3EventSource(
        #                   #bucket (Bucket) –
        #                   bucket,
        #                   #events (Sequence[EventType]) – The s3 event types that will trigger the notification.
        #                   events=[s3_.EventType.OBJECT_CREATED],
        #                 #   filters (Optional[Sequence[NotificationKeyFilter]]) – S3 object key filter rules to 
        #                 #   determine which objects trigger this event. Each filter must include a prefix and/or
        #                 #   suffix that will be matched against the s3 object key.
        #                   filters=[s3_.NotificationKeyFilter(suffix=".txt")]))
        bucket.add_event_notification(
                             s3_.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(lambdaaplication),
            s3_.NotificationKeyFilter(
                
                suffix=".txt",
            ))

        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/BucketDeployment.html  
        #uploading file to that bucket
        s3deploy_.BucketDeployment(self,'s3_resource', 
                    #sources (Sequence[ISource]) – The sources from which to deploy the contents of this bucket.
                    
                    sources=[
                           #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_deployment/Source.html
                           ##Specifies bucket deployment source.
                           s3deploy_.Source.asset('./resource',
                                     #exclude (Optional[Sequence[str]]) – (deprecated) Glob patterns to exclude from the copy.
                                     exclude =['**', '!file.txt'])],
                    ##destination_bucket (IBucket) – The S3 bucket to sync the contents of the zip file to.                                                                 
                    destination_bucket=bucket)  
    
    def lambdaaplication(self,id,asset,handler,rule):
        return lambda_.Function(self,id,
                            code=lambda_.Code.from_asset(asset),
                            runtime=lambda_.Runtime.PYTHON_3_6,
                            handler=handler,
                            timeout=Duration.seconds(30),
                                      role=rule
                                )
                                
                                
                                
                                
    def create_lambda_rule(self,CW_Access,A_S3_Access,AMZ_Access,AWSLambdaBasicExecutionRole):

        lambda_rule = aws_iam_.Role(self, "Role",                     
                                    assumed_by=aws_iam_.ServicePrincipal(AMZ_Access),
                                    description="showing logs on cloudwhatch",
                                    managed_policies=[aws_iam_.ManagedPolicy.from_aws_managed_policy_name(AWSLambdaBasicExecutionRole), #AWSLambdaBasicExecutionRole grants permissions to upload logs to CloudWatch.
                                    aws_iam_.ManagedPolicy.from_aws_managed_policy_name(CW_Access),
                                    aws_iam_.ManagedPolicy.from_aws_managed_policy_name(A_S3_Access),
                                    aws_iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')])
        return lambda_rule
        
        
    