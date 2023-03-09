import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint__6_app.ECR_stack import ECR_stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint__6_app/sprint__6_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ECR_stack(app, "sprint--6-app")
    template = assertions.Template.from_stack(stack)

def test_repository_created(): 
    app = core.App()
    stack = ECR_stack(app, "sprint--6-app")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::ECR::Repository", 1)
def test_policy_created():

    app = core.App()
    stack = ECR_stack(app, "Basit-sprint-3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Policy",1)


def test_ecs_clustor_created():
    """
    this function is used for the finding number of DynamoDB tables
    """
    app = core.App()
    stack = ECR_stack(app, "sprint--6-app")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Role", 1)    # count the resources  


