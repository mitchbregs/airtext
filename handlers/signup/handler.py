"""Message AWS Lambda handler."""
import logging
from typing import Dict

from airtext.handlers.message import MessageEvent, Incoming, Outgoing

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

    request = Request(event=event)
    controller = Controller()  # or controller = message_event.get_controller()
    controller.dispatch_request(request=request)


if __name__ == "__main__":
    # ADD
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=ADD+%2B1+%28908%29+565-1367+%40Rebecca&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=ADD+%2B1+%28908%29+5dd65-1367+%40Rebecca&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}

    # # GET
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=GET+%2B1+%28908%29+565-1367+%40Rebecca&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}

    # # # UPDATE
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=UPDATE+%2B1+%28908%29+565-1367+%40Becca&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}

    # # # DELETE
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=DELETE+%2B1+%28908%29+565-1367+%40Becca&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=DELETE+%2B1+%28908%29+565-1367&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}

    # ASK
    # MOCK_EVENT = {'body': 'ToCountry=US&ToState=NJ&SmsMessageSid=SM8f78485858368192fd6f74bcba7bae56&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM8f78485858368192fd6f74bcba7bae56&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=COMMANDS+%2B1+%28908%29+565-1367&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM8f78485858368192fd6f74bcba7bae56&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01'}

    # TO:

    MOCK_CONTEXT = {}

    main(MOCK_EVENT, MOCK_CONTEXT)
