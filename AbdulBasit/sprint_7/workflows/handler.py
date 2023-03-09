
import boto3
import json
import requests
from pathlib import Path
import os
from flask import Flask, request
from email import EmailClient

def lambda_handler(event, context):
    
    
    app = Flask(__name__)

    FILE_DIR = Path().resolve().parent
    QueueName = os.getenv('QueueName')
    ACTIONS_QUEUE = QueueName


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

    