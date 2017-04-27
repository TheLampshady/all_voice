from tests.base import TestBaseIntent
from models.user import AllVoiceUser
from models.google_home_skill import GoogleHomeRequest


class TestGoogleHome(TestBaseIntent):

    def test_google_home_skill(self):
        event = self.get_mock_google_home_event(intent="test", user_id="mr-user")

        skill = GoogleHomeRequest(event)
        self.assertEqual(skill.user, AllVoiceUser)

        self.assertEqual(skill.user_id, "mr-user")
        self.assertEqual(skill.intent_name, "test")
