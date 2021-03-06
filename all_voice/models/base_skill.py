from all_voice.models.user import AllVoiceUser


class BaseSkill(object):
    BREAK = " <break /> "
    DEFAULT_LIFESPAN = 5

    def __init__(self, *args, **kwargs):
        """
        An interface for implementing a skill. Google, Alexa and other base skills used by the
            all voice must implement all stubs to be used by child skills.
        :param args:
        :param kwargs:
        """
        self.skill_type = NotImplemented
        self.user = AllVoiceUser
        self.event = NotImplemented
        self.logger = NotImplemented
        self.parameters = NotImplemented
        self.attributes = NotImplemented
        self._contexts = NotImplemented
        self.user_id = NotImplemented
        self.intent_name = NotImplemented

    def build_response(self, speech, reprompt=None, title=None, text=None, **data):
        """
        Takse results and formats for API response
        :type speech: basestring or None
        :type reprompt: basestring or None
        :type title: basestring or None
        :type text: basestring or None
        :type data: dict
        :rtype: dict
        """
        raise NotImplementedError("Not Implemented.")

    def response(self):
        """Main class for generating a response from the event"""
        raise NotImplementedError("Not Implemented.")

    def convert_to_ssml(self, value):
        text = "<speak>%s</speak>" % value.replace("&", "and")
        return text.replace(". ", self.BREAK).replace(", ", self.BREAK)

    def add_context(self, name, parameters, lifespan=None):
        """
        Adds context to response
        :type name: str
        :type parameters: dict
        :type lifespan: int
        """
        if lifespan is None:
            lifespan = self.DEFAULT_LIFESPAN
        self._contexts[name.lower()] = {
            'parameters': parameters,
            'lifespan': lifespan
        }

    def remove_context(self, name):
        """
        Removes from context response
        :type name: str
        :return: dict
        """
        return self._contexts.pop(name.lower(), {})

    def get_context(self, name):
        """
        Gets context.
        :type name:
        :return: dict
        """
        return self._contexts.get(name.lower(), {})

    def log_error(self, error):
        self.user.log_error(self.user_id, error)

    def get_error(self):
        message = self.user.get_error(self.user_id)
        return message or "Nothing is wrong"

    def LaunchRequest(self):
        return self.build_response(
            text='Launch',
            speech="Welcome!"
        )

    def CancelIntent(self):
        return self.build_response(
            text='Cancelled',
            speech="Good Bye!"
        )

    def StopIntent(self):
        return self.build_response(
            text='Stopped',
            speech="Good Bye!"
        )

    def HelpIntent(self):
        return self.build_response(
            text='Help Intent',
            speech="Read the Manual.",
            reprompt="R T M"
        )

    def _ErrorIntent(self):
        speech = "There was an error with the intent: %s." % self.intent_name
        reprompt = "Say Diagnostic for details."
        return self.build_response(speech, reprompt, title='Error')

    def DiagnosticIntent(self):
        speech_output = self.get_error() or "Nothing is wrong"
        return self.build_response(speech_output, title="Diagnostic")
