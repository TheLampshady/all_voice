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

    def build_response(self, speech, text, reprompt=None):
        raise NotImplementedError("Not Implemented.")

    def response(self):
        """Main class for generating a response from the event"""
        raise NotImplementedError("Not Implemented.")

    def log_error(self, error):
        """Saves log to a User"""
        raise NotImplementedError("Not Implemented.")

    def get_error(self):
        """Gets log from a User"""
        raise NotImplementedError("Not Implemented.")

    def LaunchRequest(self):
        """Intent Required by some Services"""
        raise NotImplementedError("Not Implemented.")

    def HelpIntent(self):
        """Intent Required by some Services"""
        raise NotImplementedError("Not Implemented.")

    def CancelIntent(self):
        """Intent Required by some Services"""
        raise NotImplementedError("Not Implemented.")

    def StopIntent(self):
        """Intent Required by some Services"""
        raise NotImplementedError("Not Implemented.")
