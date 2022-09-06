import json
import logging
import re
from typing import Dict

from airtext.api import AirtextAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    """Creates a contact."""
    logger.info(event)
    logger.info(context)

    body = json.loads(event["body"])

    name = body["name"]
    email = body["email"]
    number = body["number"]
    area_code = body["area_code"]

    airtext = AirtextAPI()

    # Validate number format
    search = re.search(r"^\+1\d{10}$", number)
    if not search:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Invalid number provided."),
            "isBase64Encoded": False,
        }

    try:
        proxy_number = airtext.twilio.create_number(area_code=area_code)
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Error creating proxy number."),
            "isBase64Encoded": False,
        }

    try:
        member = airtext.members.create(
            proxy_number=proxy_number.phone_number
            name=name,
            email=email,
            number=number,
        )
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Error creating member."),
            "isBase64Encoded": False,
        }

    try:
        group = airtext.groups.create(
            name="all",
            member_id=member.id,
        )
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Error creating group."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": member.to_json(),
        "isBase64Encoded": False,
    }
