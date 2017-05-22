from datetime import datetime


class AllVoiceTestUtils(object):

    def get_mock_alexa_event(self, intent=None, session_id="SessionId.uuid", attributes=None, parameters=None):
        mock_event = {
            "session": {
                "sessionId": session_id,
                "application": {
                    "applicationId": "amzn1.ask.skill.1234"
                },
                "user": {
                    "userId": "user_id"
                },
                "new": False
            },
            "request": {
                "requestId": "EdwRequestId.24744310-0cfc-432e-a5fd-d5f42813b8b7",
                "locale": "en-US",
                "timestamp": "2016-12-16T16:27:31Z",
            },
            "version": "1.0"
        }

        if intent:

            mock_event["request"]["type"] = "IntentRequest"
            mock_event["request"]["intent"] = {
                "name": intent,
                "slots": {}
            }
            if parameters:
                mock_event["request"]["intent"]["slots"] = \
                    self._dict_to_slot(parameters)


        if attributes:
            mock_event["session"]["attributes"] = attributes

        return mock_event

    @staticmethod
    def _dict_to_slot(params):
        return {
            key: {"name": key, "value": value}
            for key, value in params.items()
        }


    @staticmethod
    def get_mock_google_home_event(intent=None, session_id="SessionId.uuid", user_id="1", parameters=None, attributes=None):
        now = datetime.now().isoformat()

        original_request = {
            "source": "google",
            "data": {
                "conversation": {
                    "conversation_id": "1488240997678",
                    "type": 2,
                    "conversation_token": "[]"
                },
                "user": {
                    "user_id": user_id
                },
                "surface": {
                    "capabilities": [
                        {"name": "actions.capability.AUDIO_INPUT"},
                        {"name": "actions.capability.AUDIO_OUTPUT"}
                    ]
                },
                "inputs": [{
                    "raw_inputs": [{
                        "input_type": 2,
                        "annotation_sets": [],
                        "query": "who needs help"
                    }],
                    "intent": "assistant.intent.action.TEXT",
                    "arguments": [{
                        "text_value": "who needs help",
                        "raw_text": "who needs help",
                        "name": "text"
                    }]
                }]
            }
        }

        meta_data = {
            u'intentName': u'Find News',
            u'webhookUsed': u'true',
            u'intentId': u'fc0eede5-fa41-46fe-8812-fa13adf65fef',
            u'webhookForSlotFillingUsed': u'false'
        }

        mock_event = {
            "id": "4ecf1b39-0d2b-4498-9af9-0ca2f500660a",
            "timestamp": now,
            "lang": "en",
            "originalRequest": original_request,
            "result": {
                "source": "agent",
                "resolvedQuery": "what is happening today",
                "actionIncomplete": False,
                "metadata": meta_data,
                "fulfillment": {
                    "speech": "",
                    "messages": [
                        {
                            "type": 0,
                            "speech": ""
                        }
                    ]
                },
                "score": 1
            },
            "status": {
                "code": 200,
                "errorType": "success"
            },
            "sessionId": session_id
        }

        if intent:
            mock_event["result"]["action"] = intent

        if parameters:
            mock_event["result"]["parameters"] = parameters

        if attributes:
            mock_event["result"]["contexts"] = [{
                "name": "default",
                "parameters": attributes,
                "lifespan": 99
            }]

        return mock_event


class MockLogger(object):
    @classmethod
    def get_or_insert(cls, *args, **kwargs):
        return ""

    @classmethod
    def log_error(cls, *args, **kwargs):
        return ""
