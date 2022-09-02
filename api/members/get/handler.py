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

    id_ = params.get("id")
    proxy_number = params.get("proxy_number")

    airtext = AirtextAPI()

    if id_:
        try:
            member = airtext.members.get_by_id(id=id_)
        except Exception as e:
            logger.error(e)
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps("Member not found using `id` provided."),
                "isBase64Encoded": False,
            }
    elif proxy_number:
        try:
            member = airtext.members.get_by_proxy_number(proxy_number=proxy_number)
        except Exception as e:
            logger.error(e)
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                },
                "body": json.dumps("Member not found using `proxy_number` provided."),
                "isBase64Encoded": False,
            }
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Must provide `proxy_number` or `id` parameter."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": member.to_json(),
        "isBase64Encoded": False,
    }
