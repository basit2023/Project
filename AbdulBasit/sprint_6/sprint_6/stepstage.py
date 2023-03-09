from aws_cdk import (
    # Duration,
                   
                   Stage,
                   
                  )
#we consider this like a copy of the application that we can run it multipul time
from constructs import Construct

import aws_cdk as cdk
from sprint_6.sprint_6_stack import Sprint6Stack
class StepStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        step_stage = Sprint6Stack(self,"BasitstepstageSprint6")    #here we define the stack for stepsstage
        
        
        
        
