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

    params = event["queryStringParameters"]

    airtext = AirtextAPI()
    group_id = params["group_id"]

    try:
        results = airtext.group_contacts.get_by_group_id(group_id=group_id)
        group_contacts = [row.to_dict() for row in results]
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(group_contacts, default=str),
        "isBase64Encoded": False,
    }
