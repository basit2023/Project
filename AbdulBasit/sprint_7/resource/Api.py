import boto3
import json
import requests
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)

FILE_DIR = Path().resolve().parent
SQS = boto3.client('sqs')
ACTIONS_QUEUE = SQS.get_queue_by_name(QueueName="workflow-actions")


@app.route("/<path:path>", methods=["POST"])
def webhooks_trigger(path):
    config_path = FILE_DIR / f"{path}.json"
    if config_path.is_file():
        run_workflow(path, request.json)
        return "Success!"

    return f"Workflow: {path} not found"


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
    
    
    
    
    
    
    
    
    
    