import boto3
import json
#import requests
from pathlib import Path

from workflows.email import EmailClient


def lambda_handler(event, context):
    """
    This function is triggered whenever there is a message in the SQS queue responsible for storing actions.
    We iterate through the messages and for any message which has the type email, we run the email action.
    """
    records = event["Records"]
    for record in records:
        message_data = json.loads(record["body"])
        print(message_data)

        action = message_data["action"]
        workflow_data = message_data['workflow_data']
        if action["type"] == "email":
            run_email_action(action["action_data"], workflow_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": "success",
    }


def run_email_action(action_data, workflow_data):
    recipient = action_data["recipient"]
    subject = action_data["subject"]

    email_client = EmailClient()
    email_client.send(
        subject=subject,
        recipient=recipient,
        email_data=[f"{k}: {v}" for k, v in workflow_data.items()]
    )
