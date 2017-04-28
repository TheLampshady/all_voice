from all_voice.models import AlexaRequest, AllVoiceUser

from tests.base import TestBaseIntent


class TestAlexa(TestBaseIntent):

    def test_alexa_skill(self):
        event = self.get_mock_alexa_event(intent="test")

        skill = AlexaRequest(event)
        self.assertEqual(skill.user, AllVoiceUser)

        self.assertEqual(skill.user_id, "user_id")
        self.assertEqual(skill.intent_name, "test")
