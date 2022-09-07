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
    name = body["name"]
    member_id = body["member_id"]

    try:
        group = airtext.groups.create(
            name=name,
            member_id=member_id,
        )

    except IntegrityError as e:
        logger.error(e)

        if isinstance(e.orig, UniqueViolation):
            message = "Group already exists."
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

event={'resource': '/groups', 'path': '/groups', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Host': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'Postman-Token': 'edd4e4b8-9df6-4e36-a723-df41b9350ca4', 'User-Agent': 'PostmanRuntime/7.29.2', 'X-Amzn-Trace-Id': 'Root=1-6317e984-3d3ddb332aa48460292a12fc', 'X-Forwarded-For': '68.83.59.111', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['application/json'], 'Accept-Encoding': ['gzip, deflate, br'], 'Content-Type': ['application/json'], 'Host': ['z4muss792f.execute-api.us-east-1.amazonaws.com'], 'Postman-Token': ['edd4e4b8-9df6-4e36-a723-df41b9350ca4'], 'User-Agent': ['PostmanRuntime/7.29.2'], 'X-Amzn-Trace-Id': ['Root=1-6317e984-3d3ddb332aa48460292a12fc'], 'X-Forwarded-For': ['68.83.59.111'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'p76wji', 'resourcePath': '/groups', 'httpMethod': 'POST', 'extendedRequestId': 'YEFsrFM-IAMFo2Q=', 'requestTime': '07/Sep/2022:00:44:52 +0000', 'path': '/v1/groups', 'accountId': '312590578399', 'protocol': 'HTTP/1.1', 'stage': 'v1', 'domainPrefix': 'z4muss792f', 'requestTimeEpoch': 1662511492140, 'requestId': '59e38f42-a2a3-47e4-8103-02765e22f0be', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '68.83.59.111', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.29.2', 'user': None}, 'domainName': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'apiId': 'z4muss792f'}, 'body': '{\n    "name": "miami",\n    "member_id": 12\n}', 'isBase64Encoded': False}
context={}
main(event, context)