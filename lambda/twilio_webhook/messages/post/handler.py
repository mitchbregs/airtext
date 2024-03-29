"""Message AWS Lambda handler."""
import logging
from typing import Dict

from airtext.controllers.twilio_webhooks import MessageController, MessageRequest

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
        message = MessageRequest(event=event)
        controller = MessageController(message=message)
        controller.dispatch_request()
    except Exception as e:
        logger.error(e)
        raise e

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/xml",
        },
        "body": "<Response/>",
        "isBase64Encoded": False,
    }
