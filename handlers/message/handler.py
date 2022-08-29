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
    event = {
        "body": "ToCountry=US&ToState=NJ&SmsMessageSid=SM51ca9a4410dfdde516138815c2d3dea7&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM51ca9a4410dfdde516138815c2d3dea7&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=TO+%2B19732835169%2C%40tmp%0A%0AYoooo&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM51ca9a4410dfdde516138815c2d3dea7&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01"
    }
    context = {}

    main(event, context)
