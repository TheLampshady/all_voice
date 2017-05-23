from all_voice.models.user import AllVoiceUser


class BaseSkill(object):

    def __init__(self, *args, **kwargs):
        """
        An interface for implementing a skill. Google, Alexa and other base skills used by the
            all voice must implement all stubs to be used by child skills.
        :param args:
        :param kwargs:
        """
        self.user = AllVoiceUser
        self.event = NotImplemented
        self.logger = NotImplemented
        self.parameters = NotImplemented
        self.attributes = NotImplemented
        self.user_id = NotImplemented
        self.intent_name = NotImplemented

    def build_response(self, speech, reprompt=None, title=None, text=None):
        raise NotImplementedError("Not Implemented.")

    def response(self):
        """Main class for generating a response from the event"""
        raise NotImplementedError("Not Implemented.")

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
            text='Cancel Intent',
            speech="Cancel"
        )

    def StopIntent(self):
        return self.build_response(
            text='Stop Intent',
            speech="Cancel"
        )

    def HelpIntent(self):
        return self.build_response(
            text='Help Intent',
            speech="Read the Manual.",
            reprompt="R T F M"
        )

    def _ErrorIntent(self):
        speech = "There was an error with the intent: %s." % self.intent_name
        reprompt = "Say Diagnostic for details."
        return self.build_response(speech, reprompt, title='Error')

    def DiagnosticIntent(self):
        speech_output = self.get_error() or "Nothing is wrong"
        return self.build_response(speech_output, title="Diagnostic")
