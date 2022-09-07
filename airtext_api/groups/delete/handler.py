import json
import logging
from typing import Dict

from airtext.api import AirtextAPI
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    logger.info(event)
    logger.info(context)

    body = json.loads(event["body"])

    airtext = AirtextAPI()
    name = body["name"]
    member_id = body["member_id"]

    try:
        airtext.groups.delete(name=name, member_id=member_id)
    except NoResultFound as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Group specified does not exist."),
            "isBase64Encoded": False,
        }
    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to delete group."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps("Group deleted."),
        "isBase64Encoded": False,
    }
