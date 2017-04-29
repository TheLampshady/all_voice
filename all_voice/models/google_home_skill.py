import logging
from base_skill import BaseRequest

log = logging.getLogger(__name__)


class GoogleHomeRequest(BaseRequest):

    DEFAULT_CONTEXT = "default"

    def __init__(self, event, user=None):
        super(GoogleHomeRequest, self).__init__(event, user)
        self.event = event
        if user:
            self.user = user
        result = self.event.get('result', {})
        self.contexts = result.get("contexts", [])

        self.intent_name = result.get('action', "")
        self.parameters = result.get('parameters', {})
        self.attributes = self.get_attributes(self.contexts)

        try:
            self.user_id = self.event['originalRequest']['data']['user']['user_id']
        except (KeyError, TypeError) as e:
            self.user_id = ""

    def get_attributes(self, contexts):
        for context in contexts:
            if context.get("name", "") == self.DEFAULT_CONTEXT:
                return context.get("parameters", {})

        return {}

    def attributes_to_context(self):
        return self.contexts + [{
            'name': self.DEFAULT_CONTEXT,
            'lifespan': 10,
            'parameters': self.attributes
        }]

    def build_response(self, speech, text, **kwargs):
        response = dict(
            speech=speech,
            displayText=text,
            data={'slack': text},
            source='default-webhook',
            contextOut=self.attributes_to_context()
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
        self.logger.log_error(self.user_id, error)

    def get_error(self):
        message = self.logger.get_error(self.user_id)
        return message or "Nothing is wrong"

    def LaunchRequest(self):
        return self.build_response(
            text='Launch',
            speech="Welcome!",
        )
