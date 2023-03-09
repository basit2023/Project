from aws_cdk import (
    # Duration,
                 # core as cdk,
                  aws_ecs as ecs,
                  aws_ecr as ecr,
                  aws_ecr_assets as ecr_assets
)
import aws_cdk as cdk
#import * as ecrdeploy  from cdk_ecr_deployment 
#from aws_cdk import core
import cdk_ecr_deployment as ecrdeploy 
from constructs import Construct

class ECR_stack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repositry=self.create_ecr_repositry(max_image_count=150,
                                                     rule_priority=1,
                                                     id="Basit_ecr_repo",
                                                     description="only retain 150 images")
        self.create_and_deploy_image(id="basit_image",
                                     directory='./app',
                                     d_id='DeployDockerImage',ecr_repositry=self.ecr_repositry)
    
    
    
    
     
    
    def create_ecr_repositry(self,max_image_count,rule_priority,id,description):
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/Repository.html
        repository=ecr.Repository(self, id,
            # Name for this repository. Default: Automatically generated name.
            #Enable the scan on push when creating the repository. Default: false
            #image scaning helps in identifying software vulnarabilitys in contanier images
            #Ensure that each new imagepushed to the repositry is scanned
            image_scan_on_push=True,
            #image_tag_mutability (Optional[TagMutability]) – The tag mutability setting for the repository. Default: TagMutability.MUTABLE
            #all images tags within the repositry will be immutable which will prevent them from being overwritten
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            #lifecycle_rules (Optional[Sequence[LifecycleRule]]) – Life cycle rules to apply to this registry. Default: No life cycle rules
            #lifecycle polices help with marging the lifecycle of the images in your repositaries
            #you define rules that result in the cleaning up of unused images.
            lifecycle_rules=[
                #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/LifecycleRule.html#aws_cdk.aws_ecr.LifecycleRule
                ecr.LifecycleRule(
                #description (Optional[str]) – Describes the purpose of the rule. Default: No description
                description=description,
                #max_image_count (Union[int, float, None]) – The maximum number of images to retain. Specify exactly one of maxImageCount and maxImageAge.
                max_image_count=max_image_count,
                rule_priority=rule_priority
            )
          ]
            
        )
        return repository
    def create_and_deploy_image(self,id,directory,d_id,ecr_repositry):
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assets/DockerImageAsset.html#aws_cdk.aws_ecr_assets.DockerImageAsset
        image=ecr_assets.DockerImageAsset(self, id,
            #directory (str) – The directory where the Dockerfile is stored.
            #The image directory is in the pyrest folder
            directory=directory
                )
        ecrdeploy.ECRDeployment(self, d_id, 
            src=ecrdeploy.DockerImageName(image.image_uri),
            dest=ecrdeploy.DockerImageName(f"{ecr_repositry.repository_uri}:latest"),
        );
        
        
        
        
        
        
        