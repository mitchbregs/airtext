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

    params = event["queryStringParameters"]

    airtext = AirtextAPI()
    proxy_number = params.get("proxy_number")

    try:
        results = airtext.contacts.get_by_proxy_number(proxy_number=proxy_number)
        contacts = [row.to_dict() for row in results]
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(contacts, default=str),
        "isBase64Encoded": False,
    }