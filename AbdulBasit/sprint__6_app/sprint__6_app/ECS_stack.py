from aws_cdk import (
                   #core as cdk,
                   aws_ec2 as ec2,
                   aws_ecr as ecr,
                   aws_ecs as ecs,
                   aws_logs as logs,
                   aws_iam as iam,
                   aws_elasticloadbalancingv2 as elb2,
                   
                  )
#we consider this like a copy of the application that we can run it multipul time
import aws_cdk as cdk
#from aws_cdk import core

from constructs import Construct
class ECS_stack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, repo:ecr.Repository, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.repo=repo
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/CfnOutput.html
        """
        arg:
           value (str) – The value of the property returned by the aws cloudformation describe-stacks command. 
           The value of an output can include literals, 
           parameter references, pseudo-parameters, a mapping value, or intrinsic functions.
        """
        cdk.CfnOutput(self,"repoName",value=repo.repository_name)
        
        
        self.create_ecs_clustor(max_azs=2,cluster_name="BasitFaragetCluster")
        self.create_task_defination(cpu=256,ephemeral_storage_gib=21,memory_limit_mib=512,environment ={"ENV1":"environment variable"},container_port=8081,container_name="BasitTaskContainer")
        self.create_fargate_service(desired_count=2,max_healthy_percent=100,min_healthy_percent=0,port=80,container_name="BasitTaskContainer",container_port=8081)
        
    def create_ecs_clustor(self,max_azs,cluster_name):
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ec2/Vpc.html
        #Define an AWS Virtual Private Cloud.
        #Vpc creates a VPC that spans a whole region.
        #max_azs (Union[int, float, None]) – Define the maximum number of AZs(avalibality zon) to use in this region.
        self.Vpc=ec2.Vpc(self,"ecs_vpc",max_azs=max_azs)
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/Cluster.html
        self.ecs_cluster =ecs.Cluster(self,"ECS_cluster",
            #cluster_name (Optional[str]) – The name for the cluster. Default: CloudFormation-generated name
            cluster_name=cluster_name,
            #container_insights (Optional[bool]) – If true CloudWatch Container Insights will be enabled for the cluster.
            container_insights=True,
            #enable_fargate_capacity_providers (Optional[bool]) – Whether to enable Fargate Capacity Providers.
            enable_fargate_capacity_providers=True,
            #vpc (Optional[IVpc]) – The VPC where your ECS instances will be running or your ENIs will be deployed.
            vpc=self.Vpc)
        
        
        
        
        
        
    def create_task_defination(self,cpu,ephemeral_storage_gib,memory_limit_mib,environment,container_port,container_name):
        #ECS role
        self.ecs_role=self.create_task_role()  
        #Define a CloudWatch Log Group.
        ecs_task_log=logs.LogGroup(self,"ecs_task_log_group",
            #retention (Optional[RetentionDays]) – How long, in days, the log contents will be retained.
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_logs/RetentionDays.html#aws_cdk.aws_logs.RetentionDays
            retention=logs.RetentionDays.FIVE_DAYS)
        #The details of a task definition run on a Fargate cluster.
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/FargateTaskDefinition.html
        self.fargate_task_defination=ecs.FargateTaskDefinition(self,"FargateTaskDefinition",
            #cpu (Union[int, float, None]) – The number of cpu units used by the task.
            cpu=cpu,
            #ephemeral_storage_gib (Union[int, float, None]) – The amount (in GiB) of ephemeral storage to be allocated to the task.
            ephemeral_storage_gib=ephemeral_storage_gib,
            #memory_limit_mib (Union[int, float, None]) – The amount (in MiB) of memory used by the task.
            memory_limit_mib=memory_limit_mib,
            #family (Optional[str]) – The name of a family that this task definition is registered to.
            family="ECS-Task-family",
            #task_role (Optional[IRole]) – The name of the IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
            task_role=self.ecs_role)
        self.fargate_task_defination.add_container("BasitTaskContainer",
            #container_name (Optional[str]) – The name of the container. Default: - id of node associated with ContainerDefinition.
            container_name=container_name,
            #cpu (Union[int, float, None]) – The minimum number of CPU units to reserve for the container.
            cpu=cpu,
            #memory_limit_mib (Union[int, float, None]) – The amount (in MiB) of memory to present to the container.
            memory_limit_mib=memory_limit_mib,
        
            #environment (Optional[Mapping[str, str]]) – The environment variables to pass to the container.
            environment ={"ENV1":"environment variable"},
       
        
           #essential (Optional[bool]) – Specifies whether the container is marked essential. If the essential parameter of 
           #a container is marked as true, and that container fails or stops for any reason, all other containers that are 
           #part of the task are stopped. If the essential parameter of a container is marked as false, then its failure does
           #not affect the rest of the containers in a task. 
        
           essential=True,
        
        
           #image (ContainerImage) – The image used to start a container. This string is passed directly to the Docker daemon.
           image=ecs.ContainerImage.from_ecr_repository(
               #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/ContainerImage.html
               #Reference an image in an ECR repository.
               repository=self.repo),
        #logging (Optional[LogDriver]) – The log configuration specification for the container. Default: - Containers use the same logging driver that the Docker daemon uses.
        logging=ecs.LogDriver.aws_logs(
            
            #stream_prefix (str) – Prefix for the log streams. The awslogs-stream-prefix option allows you to associate (next line)
            #a log stream with the specified prefix, the container name, and the ID of the Amazon ECS task to which the (next line)
            #container belongs. 
            
            stream_prefix="ecs_task",
            #log_group (Optional[ILogGroup]) – The log group to log to. Default: - A log group is automatically created.
            log_group=ecs_task_log),
            #port_mappings (Optional[Sequence[PortMapping]]) – The port mappings to add to the container definition.
        port_mappings=[ecs.PortMapping(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/PortMapping.html#aws_cdk.aws_ecs.PortMapping
            #container_port (Union[int, float]) – The port number on the container that is bound to the user-specified or automatically assigned host port.
            container_port=container_port,
            #protocol (Optional[Protocol]) – The protocol used for the port mapping. Valid values are Protocol.TCP and Protocol.UDP. Default: TCP
            #Transmission Control Protocol (TCP) is a standard that defines how to establish and maintain a network conversation by which applications can exchange data.
            protocol=ecs.Protocol.TCP)
          ],
        )
    
    def create_task_role(self):
        #Represents a statement in an IAM policy document.
        sts_policy=iam.PolicyStatement(
           #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/PolicyStatement.html
           #actions (Optional[Sequence[str]]) – List of actions to add to the statement. Default: - no actions
           actions=['sts:AssumeRole'],
           resources=["*"])
        cw_policy=iam.PolicyStatement(actions=['logs:*'],resources=["*"])
        tesk_role_policy_ducuments=iam.PolicyDocument(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/PolicyDocument.html
            #statements (Optional[Sequence[PolicyStatement]]) – Initial statements to add to the policy document. 
            statements=[sts_policy,cw_policy]
            
        )
        return iam.Role(self, "ecs-task-role",
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ServicePrincipal.html
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="ecs tasks role for pakage",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')],
            #inline_policies (Optional[Mapping[str, PolicyDocument]]) – A list of named policies to inline into this role.
            inline_policies=[tesk_role_policy_ducuments]
            )
        
    def create_fargate_service(self,desired_count,max_healthy_percent,min_healthy_percent,port,container_name,container_port):
        #This creates a service using the Fargate launch type on an ECS cluster.
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/FargateService.html
        service=ecs.FargateService(self, "ECSservice",
            #service_name (Optional[str]) – The name of the service. Default: - CloudFormation-generated name.
            service_name="ECSservice",
            #cluster (ICluster) – The name of the cluster that hosts the service.
            cluster=self.ecs_cluster,
            #task_definition (TaskDefinition) – The task definition to use for tasks in the service. 
            task_definition=self.fargate_task_defination,
            #desired_count (Union[int, float, None]) – The desired number of instantiations of the task definition to keep running on the service.
            desired_count=desired_count,
            #max_healthy_percent (Union[int, float, None]) – The maximum number of tasks, specified as a percentage of the Amazon ECS service’s DesiredCount value, that can run in a service during a deployment. 
            max_healthy_percent=max_healthy_percent,
            #min_healthy_percent (Union[int, float, None]) – The minimum number of tasks, specified as a percentage of the Amazon ECS service’s DesiredCount value,
            min_healthy_percent=min_healthy_percent,
        )
        #Define an Application Load Balancer.
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_elasticloadbalancingv2/ApplicationLoadBalancer.html
        elb=elb2.ApplicationLoadBalancer(self,"LB",
            #vpc (IVpc) – The VPC network to place the load balancer in.
            vpc=self.Vpc,
            #internet_facing (Optional[bool]) – Whether the load balancer has an internet-routable address. Default: false
            internet_facing=True,
            #Which subnets place the load balancer in.
            #vpc_subnets=ec2.SubnetSelection(availability_zones=["us-west-1a", "us-west-1b"]),
            
            )
           #Add a new listener to this load balancer.
        listener=elb.add_listener("listener", 
            #port (Union[int, float, None]) – The port on which the listener listens for requests. Default: - Determined from protocol if known.
            port=port
            )
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/FargateService.html
        #Use this function to create all load balancer targets to be registered in this service, add them to target groups, and attach target groups to listeners accordingly.
        service.register_load_balancer_targets(
            #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecs/EcsTarget.html
            ecs.EcsTarget(
            #container_name (str) – The name of the container.
            container_name=container_name,
            #container_port (Union[int, float, None]) – The port number of the container. Only applicable when using application/network load balancers.
            container_port=container_port,
            #new_target_group_id (str) – ID for a target group to be created.
            new_target_group_id="ECS",
            listener=ecs.ListenerConfig.application_listener(listener,
                #protocol (Optional[ApplicationProtocol]) – The protocol to use. Default: Determined from port if known
                protocol=elb2.ApplicationProtocol.HTTP
                )
                ),
            )
            
                #
        cdk.CfnOutput(self, "LoadBalancerDNS"  , value=elb.load_balancer_dns_name)
        