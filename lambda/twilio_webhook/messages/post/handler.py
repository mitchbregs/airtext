"""Message AWS Lambda handler."""
import json
import logging
from typing import Dict

from airtext.controllers.base import Request
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
        request = Request(event=event)
        controller = MessageController(request=request)
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


event = {'ToCountry': 'US', 'ToState': 'NJ', 'SmsMessageSid': 'SM4ec59f3f69160a2ee9f97eb792ab87c2', 'NumMedia': '0', 'ToCity': 'FAIRFIELD', 'FromZip': '07480', 'SmsSid': 'SM4ec59f3f69160a2ee9f97eb792ab87c2', 'FromState': 'NJ', 'SmsStatus': 'received', 'FromCity': 'BUTLER', 'Body': 'mitch', 'FromCountry': 'US', 'To': '%2B19738745273', 'ToZip': '07004', 'NumSegments': '1', 'ReferralNumMedia': '0', 'MessageSid': 'SM4ec59f3f69160a2ee9f97eb792ab87c2', 'AccountSid': 'AC30eea2e61a63d9a79888bb17f6a1f0ce', 'From': '%2B19732835169', 'ApiVersion': '2010-04-01'}
context = {}
main(event, context)