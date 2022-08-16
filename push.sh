#!/bin/bash
rm -rf .venv
python3 -m venv .venv
. .venv/bin/activate
pip install awscli
aws codeartifact login --tool twine --repository airtext-pypi-store --domain airtext-pypi --domain-owner 312590578399
pip install -e '.[pkg]'
python -m build --sdist --wheel --outdir dist/ .
twine upload --verbose -r codeartifact dist/*
# export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain airtext-pypi --domain-owner 312590578399 --query authorizationToken --output text`
# pip config set global.index-url https://aws:$CODEARTIFACT_AUTH_TOKEN@airtext-pypi-312590578399.d.codeartifact.us-east-1.amazonaws.com/pypi/airtext-pypi-store/simple/
