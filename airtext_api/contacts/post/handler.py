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
    name = body.get("name")  # NOTE: `name` is not required.

    try:
        contact = airtext.contacts.create(
            number=number,
            member_id=member_id,
            name=name,
        )
        group = airtext.groups.get_by_member_id(member_id=member_id)
        group_contact = airtext.group_contacts.create(
            contact_id=contact.id,
            group_id=group.id,
        )
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to create contact."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": contact.to_json(),
        "isBase64Encoded": False,
    }
