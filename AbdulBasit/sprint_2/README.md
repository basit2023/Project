
## Welcome to your CDK Python project!
####################################################################################################

##Sprint 1 Web Health monitoring App

A canrary in lambda function was built in AWS SDK in sprint 1, which measure the latency and avalibality of
a public application. later is was schedule to run periodically for every 1 menutes.


## Sprint 2: Web crawler with AWS SNS Service

The objective of sprint 2 is to extend the lambda function created in sprint 1 to a web-crawler that is 
running periodically on 5 minutes cadence and to write availability and latency metrics for each website
to CloudWatch. Then CloudWatch will monitor web health and set up alarms when availability or latency
falls below a prescribed threshold and alarm trigger, after triggering the alarm SNS notification is sent to
the email address.


#Feature 

* Monitors web health by measuring latency and avalibality
* publish latency and availability metrics to coludwatch
* sends notification when alarm is triggered
* write logs of the alarm into the dynamoDB table

##Code explanation After Sprint 1

#Create CloudWatch metrics

The CloudWatch uses the boto3 (SDK) which is include serval services and features to ease development.
It uses client that provides low level interface to AWS services. So, here I used the `put_metric_data()`
method for the purpose to publish the data point to amazon CloudWatch.

##generate an Alarm

The CloudWatch Alarms feature allows you to watch CloudWatch metrics and to receive notifications when
the metrics fall outside of the levels (high or low thresholds) that you configure. So, in this sprint 2,
for the better web health mentoring it generated an alarm when the availability or the latency metrics 
crossed the prescribed threshold.

##Create SNS service

In the above task, the alarm is setup when availability or latency falls below the prescribe threshold. 
When the alarm is triggered, a SNS notification is sent to the email address of web admin.




## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
