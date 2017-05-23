from mock import patch

from all_voice.models import AlexaSkill

from tests.base import TestBaseIntent


class TestErrorIntent(TestBaseIntent):

    def test_error_intent(self):
        event = self.get_mock_alexa_event(intent="fake")

        skill = AlexaSkill(event)
        response = skill.response()
        title = response['response']['card']['title']
        self.assertEqual(title, "Error")

    @patch.object(AlexaSkill, "CancelIntent")
    def test_diagnostic_intent(self, cancel_mock):
        message = "Cancel Error"
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.side_effect = ValueError(message)

        AlexaSkill(event).response()

        event = self.get_mock_alexa_event(intent="DiagnosticIntent")
        response = AlexaSkill(event).response()
        self.assertIn(message, response['response']['outputSpeech']['ssml'])
