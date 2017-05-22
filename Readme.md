# The All Voice
Python package for handling requests from Amazon and API.AI. Supoorts 
 Alexa, Google Home, Google Assistant, Slack and Web Apps.

# Installation
pip install git+https://github.com/TheLampshady/all_voice.git


# Usage

The AllVoice Base Skill allows a developer to extend a single class and inherit the functionality of
the skill associated with the service making the call. By uses dynamic parenting from different 
types of base skill (e.g. Alexa, Google Home) the request and response are handling implicitly while 
providing support for multiple devices. 

The developer can extend one class and just focus on developing actions with easy access to 
slots/parameters or session attributes. With session support, the Amazon attribute is used and a 
default case is added for API.AI

*#TODO* Add Alexa context support.

*#TODO* Add Alexa yes support to handle context of the question being answered

## Creating a Skill
Developers can create there skill by extending the AllVoice and adding their Intents as functions.
```python
from all_voice.models import AllVoice

class TalkToMeSkill(AllVoice):
    """My Skill"""

    def AwesomeIntent(self):
        """My Intent/Action"""
        return self.build_response("I am awesome.")
```


## Explicit Skills
Developers can also use a single skill class such as just Alexa
```python
from all_voice.models import AlexaSkill

class TalkToMeSkill(AlexaSkill):
    """My Skill"""

    def AwesomeIntent(self):
        """My Intent/Action"""
        return self.build_response("I am awesome.")
```


## User Objects
User objects are created by extending the `BaseUser` class. By default an AllVoice user provides 
simple logging powered by a python dict. Do not rely on this for webhooks that scale.
```python
from all_voice.models import BaseUser

class UserClass(BaseUser): pass
```

Once created, the class can be passes a a parameter to your skills init.
```python
def webhook(event):
    skill = TalkToMeSkill(event, UserClass)
```


## Testing
Developers can extend the unittest class and utils for generating JSON events fomr various services.
```python
import unittest
from all_voice.tests.utils import AllVoiceTestUtils

class TestBaseIntent(AllVoiceTestUtils, unittest.TestCase):

    def setUp(self):
        super(TestBaseIntent, self).setUp()
```


## Caveats
Since the parents are dynamic, references to class fields / methods will be correct but IDEs will
reference the unimplemented code and not the dynamic classes (Alexa / Google Home)

## Hosting
Fulfillments can be hosted on various platforms with this library. 
### App Engine
This exmaple will go through hosting your webhook in Google App Engine with Python an WebApp2
Review this link for a quickstart into google app engine.
[Google App Engine Quickstart](https://cloud.google.com/appengine/docs/standard/python/quickstart)

1. Create your 
    * config `app.yaml`
    * application `webapp2.WSGIApplication`
    * handler class `class Webhook(BaseHandler)`
    
2. Link your `app.yaml` to the `webapp2.WSGIApplication`
```python
- url: .*
  script: routes._APP
  secure: always
```

3. Add a route to your web hook handler 
    - `webapp2.Route("/webhook", handler=Webhook, name='webhook'),`
    
4. Add your skill to handler
```python
import json 
# ....
def post(self):
    event = json.loads(self.request.body)
    
    request = TalkToMeSkill(event)
    response = json.dumps(request.response())
    
    self.response.headers['Content-Type'] = 'application/json'
    return self.response.out.write(response)
```
5. Install this library for upload
`pip install -t libs git+https://github.com/TheLampshady/all_voice.git`

### Lambda
This example will provide the code for hosting a webhook on lambda functions.
A brief tutorial on creating a lmbda function
[Alexa on Lambda Function](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function#creating-a-lambda-function-for-an-alexa-skill)

1. Create a a function that takes the parameters below in a file called. `lambda_function.py`
```python
from my_skill import TalkToMeSkill

def lambda_handler(event, context={}):
    return TalkToMeSkill(event=event).response()
```

2. Install this library for upload
`pip install -t libs git+https://github.com/TheLampshady/all_voice.git`
