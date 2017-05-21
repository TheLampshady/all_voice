from alexa_skill import AlexaSkill
from google_home_skill import GoogleHomeSkill

from user import AllVoiceUser


class AllVoice(object):
    def __init__(self, event, user=None):
        super(AllVoice, self).__init__()
        self.user = user or AllVoiceUser
        if event.get("result"):
            self._device_skill = GoogleHomeSkill(event, user)
        elif event.get("request"):
            self._device_skill = AlexaSkill(event, user)
        else:
            raise ValueError("Unknown Request Type")

    def __getattr__(self, item):
        if hasattr(self._device_skill, item):
            return getattr(self._device_skill, item)
