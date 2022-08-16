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
        JSON-formatted Twilio incoming text webhook payload.
    context : `Dict`
        Provides methods and properties with information about the invocation.
        This argument is passed when Lambda runs any lambda_handler function.
    """
    logger.info(event)
    logger.info(context)

    message_event = MessageEvent(event=event)
    proxy = message_event.get_airtext_proxy()

    if proxy.member.number == message_event.from_number:
        message = Outgoing(proxy=proxy)
    else:
        message = Incoming(proxy=proxy)

    message.handle()


if __name__ == "__main__":
    MOCK_EVENT = {
        "body": (
            "ToCountry=US&"
            "ToState=NJ&"
            "SmsMessageSid=SM6e0070f7f27433fd07982cbf770d4834&"
            "NumMedia=0&"
            "ToCity=FAIRFIELD&"
            "FromZip=08817&"
            "SmsSid=SM6e0070f7f27433fd07982cbf770d4834&"
            "FromState=NJ&"
            "SmsStatus=received&"
            "FromCity=NEW+BRUNSWICK&"
            "Body=This+is+%0A%0AA+test+%0A%0ATo+see&"
            "FromCountry=US&"
            "To=%2B19738745273&"
            "ToZip=07004&"
            "NumSegments=1&"
            "ReferralNumMedia=0&"
            "MessageSid=SM6e0070f7f27433fd07982cbf770d4834&"
            "AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&"
            "From=%2B19086162013&"
            "ApiVersion=2010-04-01"
        )
    }
    # MOCK_EVENT = {
    #     "body": "ToCountry=US&ToState=NJ&SmsMessageSid=SM87a3c2404ee024723075372ada9d7a31&NumMedia=0&ToCity=FAIRFIELD&FromZip=08817&SmsSid=SM87a3c2404ee024723075372ada9d7a31&FromState=NJ&SmsStatus=received&FromCity=NEW+BRUNSWICK&Body=Test&FromCountry=US&To=%2B19738745273&ToZip=07004&NumSegments=1&ReferralNumMedia=0&MessageSid=SM87a3c2404ee024723075372ada9d7a31&AccountSid=AC30eea2e61a63d9a79888bb17f6a1f0ce&From=%2B19086162014&ApiVersion=2010-04-01"
    # }
    MOCK_CONTEXT = {}
    main(MOCK_EVENT, MOCK_CONTEXT)
