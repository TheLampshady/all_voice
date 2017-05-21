from all_voice.models import AlexaSkill


def lambda_handler(event, context={}):
    return AlexaSkill(event=event).response()
