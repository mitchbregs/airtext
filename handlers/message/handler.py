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
    MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM5324bab6a22393c7e285cf2917e06de7&NumMedia=0&ToCity=ENGLEWOOD&FromZip=90002&SmsSid=SM5324bab6a22393c7e285cf2917e06de7&FromState=CA&SmsStatus=received&FromCity=HUNTINGTON+PARK&Body=TO+9732835169%0AYo+bro&FromCountry=US&To=%2B19738745273&ToZip=07463&NumSegments=1&ReferralNumMedia=0&MessageSid=SM5324bab6a22393c7e285cf2917e06de7&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}
    MOCK_CONTEXT = {}
    main(MOCK_EVENT, MOCK_CONTEXT)