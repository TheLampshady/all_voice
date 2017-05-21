from all_voice.models import GoogleHomeSkill, AllVoiceUser

from tests.base import TestBaseIntent


class TestGoogleHome(TestBaseIntent):

    def test_google_home_skill(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeSkill(event)
        self.assertEqual(skill.user, AllVoiceUser)

        self.assertEqual(skill.user_id, "mr-user")
        self.assertEqual(skill.intent_name, "test")
