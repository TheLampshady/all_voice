from all_voice.models import AlexaRequest


def lambda_handler(event, context={}):
    return AlexaRequest(event=event).response()
