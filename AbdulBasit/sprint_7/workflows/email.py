import boto3


class EmailClient:
    SENDER = "Workflow Update <babaralibj362@gmail.com>"
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "{email_text}"

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <p>{email_text}</p>
    <hr/>
    </body>
    </html>
    """
    # The character encoding for the email.
    CHARSET = "UTF-8"

    def __init__(self):
        self.client = boto3.client("ses")

    def send(self, subject, recipient, email_data):
        """Send an email which contains AWS billing data"""
        email_text = "\n".join(email_data)
        email_html = "<br>".join(email_data)

        response = self.client.send_email(
            Destination={
                "ToAddresses": [
                    recipient,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": self.CHARSET,
                        "Data": email_html
                    },
                    "Text": {
                        "Charset": self.CHARSET,
                        "Data": email_text,
                    },
                },
                "Subject": {
                    "Charset": self.CHARSET,
                    "Data": subject,
                },
            },
            Source=self.SENDER,
        )
        return response
    
    
    
    