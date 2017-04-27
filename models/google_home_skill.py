import logging
from base_skill import BaseRequest

log = logging.getLogger(__name__)


class ApiAiRequest(BaseRequest):

    DEFAULT_CONTEXT = "default"

    def __init__(self, event):
        super(ApiAiRequest, self).__init__(event)
        self.event = event
        result = self.event.get('result', {})
        self.contexts = result.get("contexts", [])

        self.intent_name = result.get('action', "")
        self.parameters = result.get('parameters', {})
        self.attributes = self.get_attributes(self.contexts)

        try:
            self.user = self.event['originalRequest']['data']['user']['user_id']
        except (KeyError, TypeError) as e:
            self.user = None

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
            data={},
            source='spare-change-webhook',
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

    def LaunchRequest(self):
        return self.build_response(
            text='Launch',
            speech="Welcome!",
        )
