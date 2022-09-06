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
    proxy_number = params["proxy_number"]
    # member_id = params.get("member_id")

    try:
        results = airtext.groups.get_by_proxy_number(proxy_number=proxy_number)
        groups = [row.to_dict() for row in results]
    except Exception as e:
        logger.info(e)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to retrieve groups."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(groups, default=str),
        "isBase64Encoded": False,
    }
