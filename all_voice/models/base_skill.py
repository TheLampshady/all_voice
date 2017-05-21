from user import AllVoiceUser


class BaseSkill(object):

    def __init__(self, *args, **kwargs):
        self.user = AllVoiceUser
        self.event = NotImplemented
        self.logger = NotImplemented
        self.parameters = NotImplemented
        self.attributes = NotImplemented
        self.user_id = NotImplemented
        self.intent_name = NotImplemented

    def build_response(self, speech, text, reprompt=None):
        raise NotImplementedError("Not Implemented.")

    def get_slot(self, name):
        raise NotImplementedError("Not Implemented.")

    def response(self):
        raise NotImplementedError("Not Implemented.")

    def log_error(self, error):
        raise NotImplementedError("Not Implemented.")

    def get_error(self):
        raise NotImplementedError("Not Implemented.")

    def LaunchRequest(self):
        raise NotImplementedError("Not Implemented.")

    def CancelIntent(self):
        raise NotImplementedError("Not Implemented.")

    def StopIntent(self):
        raise NotImplementedError("Not Implemented.")

    def HelpIntent(self):
        raise NotImplementedError("Not Implemented.")
