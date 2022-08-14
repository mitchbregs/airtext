python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e '.[dev,pkg]'
python -m build --sdist --wheel --outdir dist/ .
aws codeartifact login --tool twine --repository airtext-pypi-store --domain airtext-pypi --domain-owner 312590578399
twine upload --verbose -r codeartifact dist/*
# export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain airtext-pypi --domain-owner 312590578399 --query authorizationToken --output text`
# pip config set global.index-url https://aws:$CODEARTIFACT_AUTH_TOKEN@airtext-pypi-312590578399.d.codeartifact.us-east-1.amazonaws.com/pypi/airtext-pypi-store/simple/