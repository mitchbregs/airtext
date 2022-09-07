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
    member_id = body["member_id"]

    try:
        group = airtext.groups.create(
            name=name,
            member_id=member_id,
        )
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to create group."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": group.to_json(),
        "isBase64Encoded": False,
    }
