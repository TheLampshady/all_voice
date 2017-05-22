import logging
from base_skill import BaseSkill

log = logging.getLogger(__name__)


class GoogleHomeSkill(BaseSkill):

    DEFAULT_CONTEXT = "default"

    def __init__(self, event, user=None):
        """
        Constructor for Google Home (API.AI) requests.
        :param event: <dict> JSON
        :param user: <BaseUser> User object
        """
        super(GoogleHomeSkill, self).__init__(event, user)
        self.event = event
        if user:
            self.user = user
        result = self.event.get('result', {})
        self.contexts = result.get("contexts", [])

        self.intent_name = result.get('action', "")
        self.parameters = result.get('parameters', {})
        self.attributes = self._get_attributes(self.contexts)

        try:
            self.user_id = self.event['originalRequest']['data']['user']['user_id']
        except (KeyError, TypeError) as e:
            self.user_id = ""

    def _get_attributes(self, contexts):
        for context in contexts:
            if context.get("name", "") == self.DEFAULT_CONTEXT:
                return context.get("parameters", {})

        return {}

    def _attributes_to_context(self):
        return self.contexts + [{
            'name': self.DEFAULT_CONTEXT,
            'lifespan': 10,
            'parameters': self.attributes
        }]

    def build_response(self, speech, text=None, **kwargs):
        response = dict(
            speech=speech,
            displayText=text or speech,
            data={
                'slack': {"text": speech}
            },
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

    def LaunchRequest(self):
        return self.build_response(
            text='Launch',
            speech="Welcome!",
        )

    def CancelIntent(self):
        return self.build_response(
            text='CancelIntent',
            speech='goodbye'
        )

    def StopIntent(self):
        return self.build_response(
            text='Stop Intent',
            speech='goodbye'
        )

    def HelpIntent(self):
        return self.build_response(
            text='Help Intent',
            speech="Read the Manual.",
            reprompt="R T F M"
        )
