from aws_cdk import (
    # Duration,
                   
                   Stage,
                   
                  )
#we consider this like a copy of the application that we can run it multipul time
from constructs import Construct

import aws_cdk as cdk
from sprint_4.sprint_4_stack import Sprint4Stack
class StepStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        step_stage = Sprint4Stack(self,"BasitstepstageSprint4")    #here we define the stack for stepsstage
        
        
        
        
