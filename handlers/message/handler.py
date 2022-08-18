"""Message AWS Lambda handler."""
import logging
from typing import Dict

from airtext.controllers import MessageController, MessageRequest

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

    request = MessageRequest(event=event)

    controller = MessageController(request=request)
    controller.dispatch_request()


if __name__ == "__main__":
    MOCK_EVENT = {
        "body": "ToCountry=US&ToState=NJ&SmsMessageSid=SMef2ee44fffff75378397f1b6d5c9efda&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SMef2ee44fffff75378397f1b6d5c9efda&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=TO+%2B19732835169%0A%0ATest&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SMef2ee44fffff75378397f1b6d5c9efda&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01"
    }

    MOCK_CONTEXT = {}
    main(MOCK_EVENT, MOCK_CONTEXT)
