import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint_7.sprint_7_stack import Sprint7Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint_7/sprint_7_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint7Stack(app, "sprint-7")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
