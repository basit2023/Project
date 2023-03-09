from aws_cdk import (
    # Duration,
                   
                   Stage,
                   
                  )
#we consider this like a copy of the application that we can run it multipul time
from constructs import Construct

import aws_cdk as cdk
from sprint__6_app.ECR_stack import ECR_stack
from sprint__6_app.ECS_stack import ECS_stack
class StepStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # step_stage_ECR = ECR_stack(self,"BasitstepstageECR_stack")    #here we define the stack for stepsstage
        # step_stage_ECS = ECS_stack(self,"BasitstepstageECR_stack")
        
        step_stage_ECR=ECR_stack(self, "BasitstepstageECRstack")
        step_stage_ECR=ECS_stack(self, "BasitstepstageECSstack", repo=step_stage_ECR.ecr_repositry)
        
        
        
        
