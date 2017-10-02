from all_voice.models import GoogleHomeSkill
from all_voice.models.user import AllVoiceUser

from tests.base import TestBaseIntent


class TestGoogleHome(TestBaseIntent):

    def test_google_home_skill(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeSkill(event)
        self.assertEqual(skill.user, AllVoiceUser)

        self.assertEqual(skill.user_id, "mr-user")
        self.assertEqual(skill.intent_name, "test")

    def test_google_home_context(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeSkill(event)

        skill.add_context("test", {"a": 1})

        result = skill.build_response("context")

        self.assertIn("contextOut", result)
        context_dict = {
            context.get('name', ""): {
                'lifespan':  context.get('lifespan'),
                'parameters':  context.get('parameters')
            }
            for context in result['contextOut']
        }
        self.assertIn("test", context_dict)
        self.assertIn("default", context_dict)
        self.assertIn("a", context_dict['test']['parameters'])

    def test_google_home_data(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeSkill(event)
        result = skill.build_response(
            "speech",
            jet={
                "test": 1
            }
        )

        self.assertIn("jet", result.get("data", {}))

