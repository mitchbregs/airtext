import json
import logging
from typing import Dict

from airtext.api import AirtextAPI
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(event: Dict, context: Dict) -> None:
    """Creates a contact."""
    logger.info(event)
    logger.info(context)

    body = json.loads(event["body"])

    airtext = AirtextAPI()
    group_id = body["group_id"]
    contact_id = body["contact_id"]

    try:
        group_contact = airtext.group_contacts.create(
            group_id=group_id,
            contact_id=contact_id,
        )

    except IntegrityError as e:
        logger.error(e)

        if isinstance(e.orig, UniqueViolation):
            message = "Group contact already exists."
        else:
            message = "Error inserting into database."

        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(message),
            "isBase64Encoded": False,
        }

    except Exception as e:
        logger.error(e)
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps("Unable to create group contact."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": group_contact.to_json(),
        "isBase64Encoded": False,
    }
