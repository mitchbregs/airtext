import os
from flask import Flask, request, abort
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/', methods=['POST'])
def reset():
    validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))
    if not validator.validate(request.url, request.form,
                              request.headers.get('X-Twilio-Signature')):
        abort(400)
    resp = MessagingResponse()
    resp.message('Hello from AWS Lambda!')
    return str(resp), 200, {'Content-Type': 'application/xml'}
