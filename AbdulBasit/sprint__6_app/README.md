
## Welcome to CDK Python project Sprint 6!

# Objective Of the Sprint 6

In this sprint,  the Amazon Elastic Container Registry (Amazon ECR) is integrated with Amazon ECS which 
allows to easily store, run, and manage container images for applications running on Amazon ECS. All need
to do is specify the Amazon ECR repository in the task definition and Amazon ECS will retrieve the 
appropriate images for the applications.

# Technology
* Docker
* Python
* AWS
* Git Hub


# Aws Services

* AWS Cloud9
* Amazon Elastic Container Service (Amazon ECS)
* AWS CloudFormation
* AWS CloudWatch
* AWS Amazon Elastic Container Registry (ECR)
* AWS IMA
* vpc
* Load Balancer


# Feature of the sprint

* Create a Docker image
* Create simple flask web-based applications
* create Amazon Elastic Container Registry (ECR) and deploy image into it.
* Create a Amazon Elastic Container Service (Amazon ECS) as a container orchestration service

# Docker Build and run commands

* Stage 1. Creating a Dockerfile
In stage 1, we create (downloade) a docker file
* Stage 2. Building an image
In stage 2, Docker images are built from Dockerfiles using the command: `$ docker build -t <filename> .`
* Stage 2, Running a Docker container
In stage 3,To run a Docker container, use the docker run command: `$ docker run <filename>`
If we add an argument with the run command, it overrides the default instruction, i.e.: `$ docker run <filename> hostname`

# Folder Structure
```
|-- .sprint__6_app
    |-- .app
    |   |----.app.py
    |   |----Dockerfile
    |   |----requirements.txt
    |----templets
    |    |---index.html
    |    |--pic.html
    |-- sprint__6_app
    |    |-- ECR_stack
    |    |-- ECS_stack
    |    |-- pipeline_stack
    |    |-- stepstage
    |-- tests
    |    |-- unit
    |        |-- test_sprint__6_app_stack.py
    |-- app.py
    |-- requirements-dev.txt
    |-- requirements.txt
    |-- README.md
 ```   
        

# Here goes setup for CDK CLI environment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Have a Nice Day Ahead!
