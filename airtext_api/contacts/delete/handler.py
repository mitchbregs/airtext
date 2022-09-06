import json
import logging
from typing import Dict

from airtext.api import AirtextAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    """Creates a contact."""
    logger.info(event)
    logger.info(context)

    body = json.loads(event["body"])

    airtext = AirtextAPI()
    number = body["number"]
    member_id = body["member_id"]

    try:
        airtext.contacts.delete(number=number, member_id=member_id)
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to delete contact."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Contact deleted."),
        "isBase64Encoded": False,
    }
