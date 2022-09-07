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

event = {'resource': '/groups', 'path': '/groups', 'httpMethod': 'DELETE', 'headers': {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Host': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'Postman-Token': 'd2a13e3e-2f0e-483f-bb70-a30371e63030', 'User-Agent': 'PostmanRuntime/7.29.2', 'X-Amzn-Trace-Id': 'Root=1-6317ef84-63c89a255398b0b96e7110ef', 'X-Forwarded-For': '68.83.59.111', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['application/json'], 'Accept-Encoding': ['gzip, deflate, br'], 'Content-Type': ['application/json'], 'Host': ['z4muss792f.execute-api.us-east-1.amazonaws.com'], 'Postman-Token': ['d2a13e3e-2f0e-483f-bb70-a30371e63030'], 'User-Agent': ['PostmanRuntime/7.29.2'], 'X-Amzn-Trace-Id': ['Root=1-6317ef84-63c89a255398b0b96e7110ef'], 'X-Forwarded-For': ['68.83.59.111'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'p76wji', 'resourcePath': '/groups', 'httpMethod': 'DELETE', 'extendedRequestId': 'YEJczEt_IAMFefg=', 'requestTime': '07/Sep/2022:01:10:28 +0000', 'path': '/v1/groups', 'accountId': '312590578399', 'protocol': 'HTTP/1.1', 'stage': 'v1', 'domainPrefix': 'z4muss792f', 'requestTimeEpoch': 1662513028953, 'requestId': '71e59996-e93f-43af-a73c-2072d688594d', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '68.83.59.111', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.29.2', 'user': None}, 'domainName': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'apiId': 'z4muss792f'}, 'body': '{\n    "name": "miami",\n    "member_id": 12\n}', 'isBase64Encoded': False}
context = {}
main(event, context)