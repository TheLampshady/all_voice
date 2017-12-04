import logging
from .base_skill import BaseSkill


log = logging.getLogger(__name__)


class AlexaSkill(BaseSkill):

    DEFAULT_CONTEXT = "contextOut"

    def __init__(self, event, user=None):
        """
        Constructor for Amazon Alexa requests.
        :param event: <dict> JSON
        :param user: <BaseUser> User object
        """
        super(AlexaSkill, self).__init__(event, user=None)
        self.skill_type = "Alexa"
        self.event = event
        if user:
            self.user = user
        intent = self.event['request'].get('intent', {})
        session = self.event.get("session", {})

        self.parameters = self.slots_to_dict(intent.get("slots", {}))
        self.attributes = session.get("attributes", {})
        self._contexts = self.attributes.get(self.DEFAULT_CONTEXT, {})
        self.user_id = self.event['session']['user']['userId']
        self.intent_name = intent.get('name')

        self.request_type = self.event['request'].get('type')

    def _save_context_to_attributes(self):
        self.attributes[self.DEFAULT_CONTEXT] = self._contexts

    def build_response(self, speech, reprompt=None, title="", text=None):
        self._save_context_to_attributes()
        response = dict(
            version='1.0',
            sessionAttributes=self.attributes,
            response=self._build_speech_response(
                response_text=speech,
                reprompt_text=reprompt,
                card_title=title,
                card_text=text or speech,
            ),
        )
        log.info(response)
        return response

    @staticmethod
    def slots_to_dict(slots):
        return {key: value.get('value') for key, value in list(slots.items())}

    def _build_speech_response(self, response_text, card_title, card_text, reprompt_text=None):
        output = dict(
            outputSpeech=dict(
                type='SSML',
                ssml=self.convert_to_ssml(response_text),
            ),
            card=dict(
                type='Simple',
                title=card_title,
                content=card_text,
            ),
            shouldEndSession=True,
        )
        if reprompt_text is not None:
            output['reprompt'] = dict(
                outputSpeech=dict(
                    type='PlainText',
                    text=reprompt_text,
                )
            )
            output['shouldEndSession'] = False
        return output

    def clean_intent_name(self):
        return self.intent_name.replace('.', '_').replace('AMAZON_', '')

    def response(self):
        try:
            if self.request_type == 'IntentRequest':
                intent_name = self.clean_intent_name()
                try:
                    return getattr(self, intent_name)()
                except Exception as e:
                    log.exception(e)
                    raise e
            elif self.request_type == "LaunchRequest":
                return self.LaunchRequest()
            return 'intentType: {r}'.format(r=self.request_type)
        except Exception as e:
            self.log_error(e.message)
            return self._ErrorIntent()


