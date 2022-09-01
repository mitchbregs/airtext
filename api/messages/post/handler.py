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
    to_number = body["to_number"]
    from_number = body["from_number"]
    body_content = body["body_content"]
    media_content = body["media_content"]
    proxy_number = body["proxy_number"]
    member_id = body["member_id"]
    command = body["command"]
    numbers = body["numbers"]
    names = body["names"]
    groups = body["groups"]
    body = body["body"]
    error = body["error"]
    error_code = body["error_code"]

    try:
        airtext.messages.create(
            to_number=to_number,
            from_number=from_number,
            body_content=body_content,
            media_content=media_content,
            proxy_number=proxy_number,
            member_id=member_id,
            command=command,
            numbers=numbers,
            names=names,
            groups=groups,
            body=body,
            error=error,
            error_code=error_code,
        )
    except Exception as e:
        logger.info(e)
        raise e

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Message created."),
        "isBase64Encoded": False,
    }
