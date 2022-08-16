# Airtext

This is a monorepo for the Airtext backend service

## Setup

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -e .  # pip install -e '.[dev,pkg,test]'
```

## Environment variables

```
export TWILIO_ACCOUNT_SID=
export TWILIO_AUTH_TOKEN=
export MESSAGES_DATABASE_URL=
```