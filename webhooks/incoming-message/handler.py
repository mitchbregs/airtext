import logging
import os
from typing import Dict
from urllib import parse

import boto3
from twilio.rest import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MESSAGE_BODY_TEMPLATE = """
{command}: {command_fields}

{message_body}
"""


def main(event: Dict, context: Dict):
    """Basic client autoresponse handler.

    Parameters
    ----------
    event : `Dict`
        JSON-formatted Twilio incoming text webhook payload.
    context : `Dict`
        Provides methods and properties with information about the invocation.
        This argument is passed when Lambda runs any lambda_handler function.

    Returns
    -------
    None
    """
    # Print for logging
    print(event)

    # Get relevant metadata
    query_string = event["body"]
    data = parse.parse_qs(qs=query_string)

    from_number = data["From"][0].replace("+", "")
    proxy_number = data["To"][0].replace("+", "")
    message_body = data["Body"][0]

    # Find client info from proxy number
    dynamodb_client = boto3.client("dynamodb")
    response = dynamodb_client.get_item(
        TableName='dev-airtext-clients',
        Key={
            "proxy_number": {
                "N": proxy_number,
            },
        },
    )

    # Get client phone number
    client_number = response["Item"]["phone_number"]["N"]

    # Perform Twilio logic
    new_message_body = MESSAGE_BODY_TEMPLATE.format(
        command="FROM",
        command_fields=from_number,
        message_body=message_body,
    )
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    twilio_client.messages.create(
        to=client_number, 
        from_=proxy_number,
        body=new_message_body,
    )
