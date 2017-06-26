#!/usr/bin/env python

import json
from flask import Flask, request, make_response

from all_voice.models import AlexaSkill

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/webhook", methods=['POST'])
def webhook():
    event = request.get_json(silent=True, force=True)

    # Process Skill
    my_skill = AlexaSkill(event)
    payload = json.dumps(my_skill.response())

    # Response
    resp = make_response(payload)
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == '__main__':
    app.run(
        host='localhost',
        port=9000,
        use_reloader=True,
    )
