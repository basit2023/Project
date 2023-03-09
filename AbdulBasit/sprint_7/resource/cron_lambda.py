

import boto3
import json
import requests
from pathlib import Path
import os
from flask import Flask, request

app = Flask(__name__)
def lambda_handler(event, context):
    FILE_DIR = Path().resolve().parent
    queue_name = os.getenv('queue_name')
    #SQS = boto3.client('sqs')
    #ACTIONS_QUEUE = SQS.get_queue_by_name(QueueName="workflow-actions")
    ACTIONS_QUEUE=queue_name
    
    
    """
    We have a function called webhooks_trigger which acts as a catch-all for incoming POST requests.
    This function checks if a workflow exists for this particular path and then runs the specified workflow.
    """
    @app.route("/<path:path>", methods=["POST"])
    
    def webhooks_trigger(path):
        config_path = FILE_DIR / f"{path}.json"
        if config_path.is_file():
            run_workflow(path, request.json)
            return "Success!"

        return f"Workflow: {path} not found"

   
    """
    The run_workflow function parses the specified workflow and enqueues any actions to SQS. The enqueued 
    message also contains any data sent to the webhook.
    """
    def run_workflow(name, workflow_data):
        workflow_path = FILE_DIR / f"{name}.json"
        with open(workflow_path) as f:
            config = json.load(f)

        actions = config["actions"]
        for action in actions:
            enqueue_action(action=action, step_data=workflow_data)


    def enqueue_action(action, step_data):
        message_data = {
            "workflow_data": step_data,
            "action": action,
        }
        ACTIONS_QUEUE.send_message(MessageBody=json.dumps(message_data))
