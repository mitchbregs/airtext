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
    name = body["name"]
    email = body["email"]
    number = body["number"]

    try:
        member = airtext.members.create(
            name=name,
            email=email,
            number=number,
        )
        group = airtext.groups.create(
            name="#all",
            member_id=member.id,
        )
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Member created."),
        "isBase64Encoded": False,
    }
