##Welcome to SkipQ Sprint1 CDK Python project!

# Web Resources Health Monitoring

## SkipQ Cohort Voyager: Sprint 1
In this project, AWS has been used to build a canary Lambda function which
measures the availability and latency of defined web resource/s when accessed. 

In this project you will find the implementation of periodic lambda function to check the availability and latency of multiple web resources (URLs). 
Using AWS CDK to create cloud infrastructure and to create a lambda function.

Technologies required to run the project are:
```
Virtual or local machine
AWS Lambda with AWS region 'us-west-1'
Github
```

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
