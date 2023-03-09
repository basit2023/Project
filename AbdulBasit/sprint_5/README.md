
## Welcome to CDK Python project Sprint 4!

# Objective Of the Sprint 5

The objective of sprint 5 is to build an image using pyresttest, and test all CRUT operations with the docker image. 
Then configure a benchmark for CRUD operation, create an environment for the pipeline and then build pipeline with docker.

# Technology
* Docker
* Python
* AWS
* Git Hub


# Aws Services

* AWS Cloud9
* AWS Lambda
* AWS CloudFormation
* AWS CloudWatch
* AWS API Getway
* AWS DynamoDB
* AWS S3 Bucket
* AWS CodePipeline 


# Feature of the sprint

* Create a Docker image
* Test all CRUD operation with Docker
* Create a configuration benchmark and find the mean for CRUD operation
* Create environment for the pipline and build pipeline with docker

# Docker Build and run commands

* Stage 1. Creating a Dockerfile
In stage 1, we create (downloade) a docker file (from thoom/pyresttest by using `from thoom/pyresttest`)
* Stage 2. Building an image
In stage 2, Docker images are built from Dockerfiles using the command: `$ docker build -t <filename> .`
* Stage 2, Running a Docker container
In stage 3,To run a Docker container, use the docker run command: `$ docker run <filename>`
If we add an argument with the run command, it overrides the default instruction, i.e.: `$ docker run <filename> hostname`

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
