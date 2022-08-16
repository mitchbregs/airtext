python -m venv .venv
source .venv/bin/activate
pip install awscli
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain airtext-pypi --domain-owner 312590578399 --query authorizationToken --output text`
export PIP_INDEX_URL=https://aws:$CODEARTIFACT_AUTH_TOKEN@airtext-pypi-312590578399.d.codeartifact.us-east-1.amazonaws.com/pypi/airtext-pypi-store/simple/
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 312590578399.dkr.ecr.us-east-1.amazonaws.com
docker build --no-cache --build-arg PIP_INDEX_URL=$PIP_INDEX_URL -t dev-airtext-messages .
docker tag dev-airtext-messages:latest 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-messages:latest
docker push 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-messages:latest
aws lambda update-function-code --function-name dev-airtext-messages-router 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-messages:latest
# TODO: aws update lambda