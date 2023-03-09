import aws_cdk as core
import aws_cdk.assertions as assertions
import urllib3
from sprint_6.sprint_6_stack import Sprint6Stack
# example tests. To run these tests, uncomment this file along with the example
# resource in sprint_3/sprint_3_stack.py
#import unittest
def test_Lambda_function_created(): 
    """
    This function will return that how many lambda function we have in this project.
    Arg:
       type (str) – the resource type.
       count (Union[int, float]) – number of expected instances.
    by default we give 1 than they return how many we have
    """
    app = core.App()
    stack = Sprint6Stack(app, "Basit-sprint-5")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Lambda::Function", 7)
# def test_s3_queue_created():
#     """
#     This function will return that how many lambda function we have in this project.
#     Arg:
#       type (str) – the resource type.
#       count (Union[int, float]) – number of expected instances.
#     by default we give 1 than they return how many we have
    

#     this function is used for the finding number of Bucket
  
#     """
#     app = core.App()
#     stack = Sprint3Stack(app, "Basit-sprint-3")
#     template = assertions.Template.from_stack(stack)
#     template.resource_count_is("AWS::S3::Bucket",1)


def test_DynamoDB_created():
    """
    this function is used for the finding number of DynamoDB tables
    """
    app = core.App()
    stack = Sprint6Stack(app, "Basit-sprint-3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 2)    # count the resources  



def test_Cloudwatch_Alarm_created():
    """
    this function is used for the finding number of CloudWatch alarm
    """
    app = core.App()
    stack = Sprint6Stack(app, "Basit-sprint-3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::CloudWatch::Alarm", 8)
# def test_S3_BucketPolicy_created():
#     """
#     Assert that a resource of the given type and properties exists in the CloudFormation template.
#     Arg:
#       type (str) – the resource type.
#       props (Any) – the ‘Properties’ section of the resource as should be expected in the template.
       
#         Match.objectLike(): this will find out if they have even partial matching on the Properties
#     """
#     app = core.App()
#     stack = Sprint3Stack(app, "Basit-sprint-3")
#     template = assertions.Template.from_stack(stack)
#     template.has_resource_properties("AWS::S3::BucketPolicy", {     # check resource properties 
#         "Bucket": assertions.Match.object_like({
#         "Ref": "abdulbasitbucketforurlE33BD6B4"
#     })

#     }
#     )
