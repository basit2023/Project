
## Welcome to CDK Python project Sprint 7!

# Objective Of the Sprint 7

In this sprint,  I’m going to build a tool like zapier using Lambda, SQS (sample queue service), and DynamoDb 
such that to add the name of the trainee to google Sheets when the trainee posts in daily standup (google sheet
integration with slack).

# Technology
* Python
* AWS
* Git Hub


# Aws Services

* AWS Cloud9
* AWS CloudFormation
* AWS IMA
* AWS SQS
* AWS DynamoDb
* AWS Lambda

# Feature of the sprint

* Build a tool like a zapier using AWS services like lambda, sqs, and dynamodb
* Create a SQS to distribute messages between components of the distribute system
* Store name of the trainee to google sheet when trinee post message on slack


# Folder Structure
```
|-- .sprint_7
    |-- .resource
    |   |----Api.py
    |   |----API_lambda
    |   |----Cron_lambda
    |   |----lambda_action
    |   |---table_scan
    |   |---function.py
    |-- sprint__7
    |    |-- sprint_7_stack.py
    |--workflows    
    |    |-- Api.py
    |    |-- email.py
    |    |-- handler.py
    |    |-- test-webhook.json
    |-- tests
    |    |-- unit
    |        |-- test_sprint_7_app_stack.py
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
