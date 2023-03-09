"""
#!/usr/bin/env python3
import os
#from aws_cdk import core as cdk
from constructs import Construct
#from aws_cdk import core
#import aws_cdk.cx_api
#import aws_cdk as cdk
import aws_cdk as cdk

from sprint__6_app.ECR_stack import ECR_stack
from sprint__6_app.ECS_stack import ECS_stack

app = cdk.App()
cdk.Tags.of(app).add("cohort", "Voyager")
cdk.Tags.of(app).add("name", "Abdul Basit")
ecr_stack=ECR_stack(app, "BasitECRstack",env=cdk.Environment(account='315997497220', region='us-east-2'))
ecs_stack=ECS_stack(app, "BasitECSstack", repo=ecr_stack.ecr_repositry,env=cdk.Environment(account='315997497220', region='us-east-2')
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
ecs_stack.add_dependency(ecr_stack, "All contanier dependency should be there")
app.synth()

"""








#!/usr/bin/env python3
import os
#from aws_cdk import core as cdk
from constructs import Construct
#from aws_cdk import core
#import aws_cdk.cx_api
#import aws_cdk as cdk
import aws_cdk as cdk

# from sprint__6_app.ECR_stack import ECR_stack
# from sprint__6_app.ECS_stack import ECS_stack
from sprint__6_app.pipeline_stack import PipelineStack

app = cdk.App()
cdk.Tags.of(app).add("cohort", "Voyager")
cdk.Tags.of(app).add("name", "Abdul Basit")
PipelineStack(app, "BasitPipeLineapp",
# ecr_stack=ECR_stack(app, "BasitECRstack",env=cdk.Environment(account='315997497220', region='us-east-2'))
# ecs_stack=ECS_stack(app, "BasitECSstack", repo=ecr_stack.ecr_repositry,env=cdk.Environment(account='315997497220', region='us-east-2')
#     # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
#ecs_stack.add_dependency(ecr_stack, "All contanier dependency should be there")
app.synth()
