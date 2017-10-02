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
        context_dict = self.context_to_dict(result)

        self.assertIn("test", context_dict)
        self.assertIn(GoogleHomeSkill.DEFAULT_CONTEXT, context_dict)
        self.assertIn("a", context_dict['test']['parameters'])

        event2 = self.get_mock_google_home_event(
            intent="test",
            user_id="mr-user",
            contexts=result.get('contextOut') or []
        )
        skill2 = GoogleHomeSkill(event2)
        self.assertTrue(skill2.get_context("test"))

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

    def test_google_home_attributes(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeSkill(event)
        skill.attributes['attr'] = 1
        result = skill.build_response("speech")

        context_dict = self.context_to_dict(result)
        self.assertIn(GoogleHomeSkill.DEFAULT_CONTEXT, context_dict)
        attributes = context_dict.get(GoogleHomeSkill.DEFAULT_CONTEXT)
        self.assertIn("attr", attributes.get("parameters"))

        event2 = self.get_mock_google_home_event(
            intent="test",
            user_id="mr-user",
            contexts=result.get('contextOut') or []
        )
        skill2 = GoogleHomeSkill(event2)
        self.assertEquals(skill2.attributes.get("attr"), 1)
