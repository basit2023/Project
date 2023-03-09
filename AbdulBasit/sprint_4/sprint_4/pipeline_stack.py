# this stack is used to deploy cdk app atomatically
from aws_cdk import (
    # Duration,
                  Stack,
                  aws_iam as aws_iam_,
                  pipelines as pipelines_, 
                  
                  aws_codepipeline_actions as action_
                  )
import aws_cdk as cdk
from constructs import Construct
from sprint_4.stepstage import StepStage
class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ##############################################################################
        #******************** Source code  *****************************
        #############################################################################
        
        """
        #source code at github
        #A CDK Pipeline that uses CodePipeline to deploy CDK apps.
        Arg:
          repo_string (str): to add repository
          authentication (Optional[SecretValue]) – A GitHub OAuth token to use for authentication.
          branch(str): present the branch to repository
          GitHubTrigger: If and how the GitHub source action should be triggered.
          The first stage of the pipeline retrieves a source artifact (an AWS CloudFormation template and its
          configuration files) from a repository.
        """
        source=pipelines_.CodePipelineSource.git_hub("abdul22skipq/Voyager","main",
                                                    authentication=cdk.SecretValue.secrets_manager("Sprint3/BST/Toke"),
                                                    trigger=action_.GitHubTrigger('POLL') #trigger repeatedly
                                                    )
        
        
        ############################################################################################
        ###############################  Built Step  #############################
        ###########################################################################################
        """
         Installation commands to run before the regular commands. For deployment engines that support it, install commands will be 
         classified differently in the job history from the regular
         
         primary_output_directory (Optional[str]) – The directory that will contain the primary output fileset.
         In the second stage, the pipeline creates a test stack
         
        """
        synth=pipelines_.ShellStep("Synth",input=source,
            
                                  commands=[
                                                    "ls && cd AbdulBasit/sprint_4/", 
                                                     "pip install -r requirements.txt",
                                                     
                                                     "npm install -g aws-cdk",
                                                     "cdk synth"
                                                     
                                              ],
                                                      primary_output_directory="AbdulBasit/sprint_4/cdk.out"
                                 )          
        Pipeline = pipelines_.CodePipeline(self, "Pipeline", synth=synth)
        ###############################################################################################################
        #******************************  step 3   ***********************************
        ###############################################################################################################
        # instantiating the step stag for beta and for production
        beta=StepStage(self,"beta") 
        prod=StepStage(self,"Prod")    #production 
        
        # unit test
     
        unit_test=pipelines_.CodeBuildStep("unit_test",  commands=["ls && cd AbdulBasit/sprint_4/", 
                                                     "pip install -r requirements-dev.txt",
                                                     'python -m pytest -vv tests/'], input=source)    #insted of pytest i added the other command because I was facing issue with pytest
                                                     
                                                     
                                                     
                                                     
                                                     
                                                     
                                                     
                                                     
       ##################################################################################################################
       ###******************** Integration test *****************************************
       ###############################################################################################################
        integraion_test=pipelines_.CodeBuildStep("integration_test",  commands=["ls && cd AbdulBasit/sprint_4/", 
                                                "pip install -r requirements.txt",
                                                'python3 resource/Integration_test_api.py'], input=source)                #this is the integration test
        
        Pipeline.add_stage(beta  ,pre=[unit_test],post=[integraion_test])      #pre is unit test and post is integration test
                              
                              
                              
                              
                              
                              
                              
                              
                              
                              
        ##########################################################################################
        #********************* Production Stage ***************************
        #########################################################################################
        """
        #the Pipeline will be paused waiting for a human to resume it
        In the third stage, the pipeline creates a change set against a production stack, and then waits for your approval.
 
        In initial run, it won't have a production stack. The change set shows all of the resources 
        that AWS CloudFormation will create. If you approve, this stage executes the change set and builds your production stack.
        """
        Pipeline.add_stage(prod,pre=[pipelines_.ManualApprovalStep("PromoteToProd")])  
        
