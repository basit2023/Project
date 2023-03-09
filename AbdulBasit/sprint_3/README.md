##Welcome to SkipQ Sprint3 CDK Python project!

## SkipQ Cohort Voyager: Sprint 3

## Objective of the sprint

The objective of the sprint 3 is to create multi-stage pipeline having Beta/Gamma and Prod 
stage using CDK, and deploy the code. Each stage must have bake Times, code-review and test
blockers. Write unit/integration tests for the web crawler. Emit CloudWatch metrics and alarms
for operational health of the web crawler, including memory and time-to-process each crawler run.
Automate rollback to the last build if metrics are in alarm. 


## Features

● CodePipeline for build and test, CodeDeploy for CD

● Integrate AWS CodePipeline with GitHub

● Automated testing using PyTest running

● Build a release process by writing merge-blocking automated tests for the canary onCodePipeline

● Build operational CloudWatch metrics for web crawler

● Write rollback automation allowing rollback to last build

● Setup beta and prod environments in CodePipeline and deploy using CodeDeploy

#Technologies required to run the project are:

```
Virtual or local machine
AWS Lambda with AWS region 'us-west-1'
AWS CodePipeline
AWS S3 Bucket
AWS Secret manager
AWS CloudFormation
Github
```
# Short overview of the Sprint 3 code:
There are three stacks in the sprint-3 folder, One is the main stack which is the  ```sprint_3_stack.py``` is 
instantiated to the ```stepstage.py``` and then this stack is instantiated to the ```pipeline_stack.py```. In 
the end, this ```App.py``` is passed to ```pipeline_stack.py``` stack.

# Here goes setup for CDK CLI environment
Check and update your python package to python3 
and check and intall latest version of CLI.

To check python version
```
$ cd python --version
```
To update python version, add `alias python='/usr/bin/python3`


For CLI version
```
$ aws --version
```

Update and install latest CLI version
```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" 
$ unzip awscliv2.zip
$ sudo ./aws/install
```

Clone the forked repo to your cloud 9 instance
   ```
   git clone <url of the forked repo>
   
   ```
  
Change directory ```cd Voyager```
Create a new folder inside Voyager 
  ```
  mkdir <yourname>
  cd <yourname>
  
  ```
Create a new folder for each new sprint inside your named folder 
```
mkdir sprint1_<yourname>
cd sprint1_<yourname>
```
Run the following commands to initialize CDK project in Python in the 
current directory, activate virtualenv and to install required dependencies and modules
```
$ cdk init app --language python 
$ source .venv/bin/activate
$ pip install aws-cdk.core==1.135.0
$ pip install -r requirements.txt 
$ nvm install v16.3.0 && nvm use v16.3.0 && nvm alias default v16.3.0
$ npm install -g aws-cdk 
$ export PATH=$PATH:$(npm get prefix)/bin
$ venv/bin/pip3.6 install -r requirements.txt
```

Write code
Commit and push the code using
```
git add .
git commit -m "some message"
git push
```
At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

## Useful commands
 * ```cdk ls```          list all stacks in the app
 * ```cdk synth```       emits the synthesized CloudFormation template
 * ```cdk deploy```      deploy this stack to your default AWS account/region
 * ```cdk diff```        compare deployed stack with current state
 * ```cdk docs```        open CDK documentation
Have a Nice day ahead!
