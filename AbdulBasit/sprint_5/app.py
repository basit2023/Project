
import os

import aws_cdk as cdk
from sprint_5.pipeline_stack import PipelineStack


app = cdk.App()
cdk.Tags.of(app).add("cohort", "Voyager")
cdk.Tags.of(app).add("name", "Abdul Basit")
#Sprint3Stack(app, "BasitSprint3Stack",
PipelineStack(app, "BasitPipeLineSprintfive",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='315997497220', region='us-east-2'),
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
app.synth()
"""
#!/usr/bin/env python3

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from sprint_5.sprint_5_stack import Sprint5Stack


app = cdk.App()
cdk.Tags.of(app).add("cohort", "Voyager")
cdk.Tags.of(app).add("name", "Abdul Basit")
Sprint5Stack(app, "BasitSprint5Stack",
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

app.synth()
"""