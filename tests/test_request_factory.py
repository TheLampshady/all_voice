from mock import patch
from all_voice.models import AlexaSkill, BaseSkill, get_all_voice


from tests.base import TestBaseIntent


class TestSkillFactory(TestBaseIntent):

    def test_get_skill_returns_alexa(self):
        event = self.get_mock_alexa_event()

        class MockClass(BaseSkill): pass

        skill = get_all_voice(MockClass, event)

        self.assertIn("convert_to_ssml", dir(skill), "Skill did not extent Alexa")
        self.assertNotIn("convert_to_ssml", dir(MockClass),
                         "Skill was permanently updated.")

    def test_get_skill_returns_google_home(self):
        event = self.get_mock_google_home_event()

        class MockClass(BaseSkill): pass

        skill = get_all_voice(MockClass, event)

        self.assertIn("DEFAULT_CONTEXT", dir(skill), "Skill did not extent Google")
        self.assertNotIn("DEFAULT_CONTEXT", dir(MockClass),
                         "Skill was permanently updated.")

    @patch.object(AlexaSkill, "CancelIntent")
    def test_get_skill_accesses_parent_class(self, cancel_mock):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.return_value = {"test": 1}
        class MockClass(BaseSkill):
            def CancelIntent(self):
                return super(type(self), self).CancelIntent()

        response = get_all_voice(MockClass, event).response()

        self.assertTrue(response.get("test"))
        cancel_mock.assert_called_once()
