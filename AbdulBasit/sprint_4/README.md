
## Welcome to CDK Python project Sprint 4!

# Public CRUD API Gateway endpoint for the web crawler

# Objective Of the Sprint 4

The objective of the sprint 4 is to Build a public CRUD API Gateway endpoint for the web crawler to create/read/update/delete the target list containing the list of
websites/webpages to crawl. For this First, move the json file to S3 and trigger the lambda to read data to database (DynamoDB). Then implement CRUD RESTcommands on DynamoDB 
entries. Extend tests in each stage to cover the CRUD operations andDynamoDB read/write time.

# Technology

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

* Create RESTful API Gateway interface for web crawler CRUD operations
* Write a Python Function to implement business logic of CRUD into DynamoDB
* Extend tests and prod/beta CI/CD pipelines in CodeDeploy / CodePipeline
* Use CI/CD to automate multiple deployment stages (prod vs beta)

# Short overview of the Sprint 4 code:
There are three stacks in the sprint-4 folder, One is the main stack which is the  ```sprint_4_stack.py``` is 
instantiated to the ```stepstage.py``` and then this stack is instantiated to the ```pipeline_stack.py```. In 
the end, this ```App.py``` is passed to ```pipeline_stack.py``` stack.
 In the main stack ```sprint_4_stack.py```, there are four lambdas, Web health lambda which is used to find the health of a specified web,
 DynamoDB lambda which is used to write data to table from alarms, DynamoDb lambda which is triggering from S3 bucket, and API Gatwey lambda.
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
