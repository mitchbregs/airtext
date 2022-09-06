import json
import logging
from typing import Dict

from airtext.api import AirtextAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    """Gets groups by proxy number."""
    logger.info(event)
    logger.info(context)

    body = json.loads(event["body"])

    airtext = AirtextAPI()
    group_id = body["group_id"]
    contact_id = body["contact_id"]

    try:
        group_contact = airtext.group_contacts.delete(
            group_id=group_id, contact_id=contact_id
        )
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Group contact deleted."),
        "isBase64Encoded": False,
    }

    body = json.loads(event["body"])

    airtext = AirtextAPI()
    group_id = body["group_id"]

    try:
        group = airtext.groups.delete(
            group_id=group_id,
        )
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Group deleted."),
        "isBase64Encoded": False,
    }
