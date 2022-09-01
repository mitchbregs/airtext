#!/bin/bash
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker system prune --force
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate
pip install awscli
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain airtext-pypi --domain-owner 312590578399 --query authorizationToken --output text`
export PIP_INDEX_URL=https://aws:$CODEARTIFACT_AUTH_TOKEN@airtext-pypi-312590578399.d.codeartifact.us-east-1.amazonaws.com/pypi/airtext-pypi-store/simple/
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 312590578399.dkr.ecr.us-east-1.amazonaws.com
docker build --no-cache --build-arg PIP_INDEX_URL=$PIP_INDEX_URL -t dev-airtext-api-group-contacts-get .
docker tag dev-airtext-api-group-contacts-get:latest 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-api-group-contacts-get:latest
docker push 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-api-group-contacts-get:latest
# aws lambda update-function-code --function-name dev-group-contacts-get --image-uri 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-api-group-contacts-get:latest