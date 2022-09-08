"""Message AWS Lambda handler."""
import json
import logging
from typing import Dict

from airtext.controllers.twilio_webhooks import MessageController

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    """Basic client autoresponse handler.

    Parameters
    ----------
    event : `Dict`
        Twilio incoming SMS message webhook payload.
    context : `Dict`
        Provides methods and properties with information about the invocation.
        This argument is passed when Lambda runs any lambda_handler function.
    """
    logger.info(event)
    logger.info(context)

    try:
        request = MessageRequest(event=event)
        controller = MessageController(request=request)
        controller.dispatch_request()
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/xml",
            },
            "body": "<Response/>",
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/xml",
        },
        "body": "<Response/>",
        "isBase64Encoded": False,
    }
