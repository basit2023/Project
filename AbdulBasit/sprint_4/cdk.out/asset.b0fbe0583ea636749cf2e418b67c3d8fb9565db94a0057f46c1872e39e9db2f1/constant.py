URL_TO_MONITOR=['www.skipq.org','www.fiverr.com']
#URL_TO_MONITOR='www.skipq.org'
Namespace='AbdulBasit_webheathlambdametrics'
matric_name_avalibality='URL_Avalibality'
matric_name_latancy='URL_latency'
CloudWach='CloudWatchFullAccess'
Dynamodbpolicy="AmazonDynamoDBFullAccess"
Threshold_Avalibality=1
Threshold_latency=0.25
TOPIC='Alarm Alert!'
Email_Address="abdul.basit.skipq@gmail.com"
Table='My_table_for_alarm_logs'
Table_s3='Basittable'
PERIOD = 1
CW_Access="CloudWatchFullAccess"
A_S3_Access="AmazonS3FullAccess"
AMZ_Access="lambda.amazonaws.com"
AWSLambdaBasicExecutionRole='service-role/AWSLambdaBasicExecutionRole'
test_url="https://frhhcggz8c.execute-api.us-west-1.amazonaws.com/prod"
put1="https://frhhcggz8c.execute-api.us-west-1.amazonaws.com/prod/put"
Payload={#'link':'www.basit.com',
        #'link':'www.youtube.com',
        #'link':'www.skipq.org',
        'link':{'S':'www.ali.com'}}