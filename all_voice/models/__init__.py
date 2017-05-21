
from base_skill import BaseSkill
from alexa_skill import AlexaSkill
from google_home_skill import GoogleHomeSkill
from .user import BaseUser, AllVoiceUser


__all__ = [
    "get_all_voice", "AlexaSkill", "GoogleHomeSkill", "BaseSkill", "BaseUser", "AllVoiceUser"
]


def get_skill(skill_class, event, user=None):
    if event.get("result"):
        request_class = GoogleHomeSkill
    elif event.get("request"):
        request_class = AlexaSkill
    else:
        raise ValueError("Unknown Request Type")
    skill = type(
        'Skill',
        (request_class,),
        dict(skill_class.__dict__)
    )
    return skill(event, user)


get_all_voice = get_skill
