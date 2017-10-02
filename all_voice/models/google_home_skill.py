import logging
from .base_skill import BaseSkill

log = logging.getLogger(__name__)


class GoogleHomeSkill(BaseSkill):

    DEFAULT_CONTEXT = "default_attributes"

    def __init__(self, event, user=None, ssml=True):
        """
        Constructor for Google Home (API.AI) requests.
        :param event: <dict> JSON
        :param user: <BaseUser> User object
        """
        super(GoogleHomeSkill, self).__init__(event, user)
        self.skill_type = "APIAI"
        self.event = event
        self.ssml = ssml
        self._contexts = {}

        if user:
            self.user = user
        result = self.event.get('result', {})
        self._parse_context(result)
        self.intent_name = result.get('action', "")
        self.parameters = result.get('parameters', {})
        self.attributes = self._get_attributes(self._contexts)

        try:
            self.user_id = self.event['originalRequest']['data']['user']['user_id']
        except (KeyError, TypeError) as e:
            self.user_id = ""

    def _parse_context(self, result):
        """
        Converts Request JSON to dict.
        :param result:
        :return:
        """
        contexts = result.get("contexts", [])
        for context in contexts:
            self.add_context(
                context.get("name", ""),
                context.get("parameters", {}),
                context.get("lifespan", self.DEFAULT_LIFESPAN)
            )

    def _get_attributes(self, contexts):
        context = contexts.get(self.DEFAULT_CONTEXT) or {}
        return context.get("parameters") or {}

    def _attributes_to_context(self):
        self.add_context(self.DEFAULT_CONTEXT, self.attributes, 10)

        return [
            {
                'name': key,
                'lifespan': value.get("lifespan", self.DEFAULT_LIFESPAN),
                'parameters': value.get("parameters", {})
            }
            for key, value in self._contexts.items()
        ]

    def build_response(self, speech, text=None, **data):
        """

        :param speech: Test to speech to ssml
        :param text: Display text to respond
        :param data: key, property pairs for 3rd party responses
        :return:
        """
        data['slack'] = {"text": text or speech}

        if self.ssml:
            data['google'] = {
                "expect_user_response": True,
                "is_ssml": True,
                "no_input_prompts": [
                    [{'ssml': speech}]
                ]
            }
        response = dict(
            speech=speech,
            displayText=text or speech,
            data=data,
            source='default-webhook',
            contextOut=self._attributes_to_context()
        )
        log.info(response)
        return response

    def response(self):
        try:
            return getattr(self, self.intent_name)()
        except Exception as e:
            log.exception(e)
            raise e

    def log_error(self, error):
        self.user.log_error(self.user_id, error)

    def get_error(self):
        message = self.user.get_error(self.user_id)
        return message or "Nothing is wrong"
