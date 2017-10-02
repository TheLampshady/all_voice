from all_voice.models import AlexaSkill
from all_voice.models.user import AllVoiceUser

from tests.base import TestBaseIntent


class TestAlexa(TestBaseIntent):

    def test_alexa_skill(self):
        event = self.get_mock_alexa_event(intent="test")

        skill = AlexaSkill(event)
        self.assertEqual(skill.user, AllVoiceUser)

        self.assertEqual(skill.user_id, "user_id")
        self.assertEqual(skill.intent_name, "test")

    def test_alexa_context(self):
        event = self.get_mock_alexa_event(intent="test", user_id="mr-user")

        skill = AlexaSkill(event)

        skill.add_context("test", {"a": 1})

        result = skill.build_response("context")
        context_dict = result['sessionAttributes'].get('contextOut')
        self.assertTrue(context_dict)
        self.assertIn("test", context_dict)
        self.assertIn("a", context_dict['test']['parameters'])
