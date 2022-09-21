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
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : True,
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*",
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
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : True,
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*",
            },
            "body": json.dumps("Error creating proxy number."),
            "isBase64Encoded": False,
        }

    try:
        member = airtext.members.create(
            proxy_number=proxy_number.phone_number,
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
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : True,
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*",
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
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : True,
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*",
            },
            "body": json.dumps("Error creating group."),
            "isBase64Encoded": False,
        }

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods" : "OPTIONS,POST",
            "Access-Control-Allow-Credentials" : True,
            "Access-Control-Allow-Origin" : "*",
            "X-Requested-With" : "*",
        },
        "body": member.to_json(),
        "isBase64Encoded": False,
    }


event = {'resource': '/members', 'path': '/members', 'httpMethod': 'POST', 'headers': {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/json', 'Host': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'Postman-Token': '256e7d65-897c-43a2-abc8-87d829dac0d6', 'User-Agent': 'PostmanRuntime/7.29.2', 'X-Amzn-Trace-Id': 'Root=1-632a5c1e-32de0a6912bd27df68399988', 'X-Forwarded-For': '68.83.59.111', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['application/json'], 'Accept-Encoding': ['gzip, deflate, br'], 'Content-Type': ['application/json'], 'Host': ['z4muss792f.execute-api.us-east-1.amazonaws.com'], 'Postman-Token': ['256e7d65-897c-43a2-abc8-87d829dac0d6'], 'User-Agent': ['PostmanRuntime/7.29.2'], 'X-Amzn-Trace-Id': ['Root=1-632a5c1e-32de0a6912bd27df68399988'], 'X-Forwarded-For': ['68.83.59.111'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 'vbbph3', 'resourcePath': '/members', 'httpMethod': 'POST', 'extendedRequestId': 'YyNU1GyyIAMF-ig=', 'requestTime': '21/Sep/2022:00:34:38 +0000', 'path': '/v1/members', 'accountId': '312590578399', 'protocol': 'HTTP/1.1', 'stage': 'v1', 'domainPrefix': 'z4muss792f', 'requestTimeEpoch': 1663720478714, 'requestId': '53c13a18-96c9-423e-86af-2b73fad0b3fe', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '68.83.59.111', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.29.2', 'user': None}, 'domainName': 'z4muss792f.execute-api.us-east-1.amazonaws.com', 'apiId': 'z4muss792f'}, 'body': '{\n    "name": "L&L Vending",\n    "email": "me@leonkozlowski.com",\n    "number": "\u202d+19735133995\u202c",\n    "area_code": "307"\n}', 'isBase64Encoded': False}
context= {}

main(event, context)