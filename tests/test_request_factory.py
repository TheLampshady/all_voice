from mock import patch
from tests.base import TestBaseIntent
from models.base_skill import BaseRequest
from models.alexa_skill import AlexaRequest


class TestSkillFactory(TestBaseIntent):

    def test_get_skill_returns_alexa(self):
        event = self.get_mock_alexa_event()

        class MockClass(BaseRequest): pass

        skill = BaseRequest.get_skill(MockClass, event)

        self.assertIn("convert_to_ssml", dir(skill), "Skill did not extent Alexa")
        self.assertNotIn("convert_to_ssml", dir(MockClass),
                         "Skill was permanently updated.")

    def test_get_skill_returns_google_home(self):
        event = self.get_mock_google_home_event()

        class MockClass(BaseRequest): pass

        skill = BaseRequest.get_skill(MockClass, event)

        self.assertIn("DEFAULT_CONTEXT", dir(skill), "Skill did not extent Google")
        self.assertNotIn("DEFAULT_CONTEXT", dir(MockClass),
                         "Skill was permanently updated.")

    @patch.object(AlexaRequest, "CancelIntent")
    def test_get_skill_accesses_parent_class(self, cancel_mock):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.return_value = {"test": 1}
        class MockClass(BaseRequest):
            def CancelIntent(self):
                return super(type(self), self).CancelIntent()

        response = BaseRequest.get_skill(MockClass, event).response()

        self.assertTrue(response.get("test"))
        cancel_mock.assert_called_once()