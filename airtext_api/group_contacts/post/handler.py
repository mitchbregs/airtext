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
    group_id = body["group_id"]
    contact_id = body["contact_id"]

    try:
        group_contact = airtext.group_contacts.create(
            group_id=group_id,
            contact_id=contact_id,
        )
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to create group contact."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": group_contact.to_json(),
        "isBase64Encoded": False,
    }
