from base_skill import BaseSkill
from alexa_skill import AlexaSkill
from google_home_skill import GoogleHomeSkill


class AllVoice(BaseSkill):
    def __init__(self, event, user=None):
        """
        Dynamic based class for handling requests from various devices and NLP services
        :param event: dict JSON request from api
        :param user: BaseUser User class for logging and skill usage
        """
        if event.get("result"):
            skill_class = GoogleHomeSkill
        elif event.get("request"):
            skill_class = AlexaSkill
        else:
            raise ValueError("Unknown Request Type")

        self.__class__.__bases__ += (skill_class,)
        super(AllVoice, self).__init__(event, user)
