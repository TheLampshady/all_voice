from mock import patch
from all_voice.models import AlexaSkill
from all_voice.models.all_skill import AllVoice

from tests.base import TestBaseIntent


class TestSkillFactory(TestBaseIntent):

    def setUp(self):
        class MockClass(AllVoice):
            pass
        self.MockClass = MockClass

    def test_get_skill_returns_alexa(self):
        event = self.get_mock_alexa_event()

        skill = self.MockClass(event)
        self.assertIn("convert_to_ssml", dir(skill), "Skill did not extent Alexa")
        self.assertNotIn("DEFAULT_CONTEXT", dir(skill), "Skill extended google.")

    def test_skill_classes_extension_is_temporary(self):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        event2 = self.get_mock_google_home_event(intent="CancelIntent")

        class MockClass(AllVoice):
            def CancelIntent(self):
                return super(AllVoice, self).CancelIntent()

        skill = MockClass(event2)
        skill.response()

        skill = self.MockClass(event)
        response = skill.response()
        text = response['response']['outputSpeech']['ssml']
        self.assertIn(AlexaSkill.CANCEL, text, "Intent was not called")

    def test_get_skill_returns_google_home(self):
        event = self.get_mock_google_home_event()

        skill = self.MockClass(event)

        self.assertIn("DEFAULT_CONTEXT", dir(skill), "Skill did not extent Google")
        self.assertNotIn("convert_to_ssml", dir(skill), "Skill extented Alexa")

    def test_get_skill_accesses_parent_class(self):
        event = self.get_mock_alexa_event(intent="LaunchRequest")

        skill = self.MockClass(event)
        self.assertEqual(skill.intent_name, "LaunchRequest")

        response = skill.response()
        self.assertTrue(response.get("response"), "No Response returned")

    @patch.object(AlexaSkill, "CancelIntent")
    def test_all_voice_calls_parent(self, cancel_mock):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.return_value = {"test": 1}

        skill = self.MockClass(event)
        response = skill.CancelIntent()

        self.assertEqual(response.get("test"), 1)
        cancel_mock.assert_called_once()

    @patch.object(AlexaSkill, "CancelIntent")
    def test_all_voice_calls_super(self, cancel_mock):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.return_value = {"test": 1}

        class MockClass(AllVoice):
            def CancelIntent(self):
                return super(AllVoice, self).CancelIntent()

        skill = MockClass(event)
        response = skill.CancelIntent()

        self.assertEqual(response.get("test"), 1)
        cancel_mock.assert_called_once()

    @patch.object(AlexaSkill, "CancelIntent")
    def test_all_voice_override(self, cancel_mock):
        event = self.get_mock_alexa_event(intent="CancelIntent")
        cancel_mock.return_value = {"test": 1}

        class MockClass(AllVoice):
            def CancelIntent(self):
                return {"test": 2}

        skill = MockClass(event)
        response = skill.CancelIntent()

        self.assertEqual(response.get("test"), 2)
        cancel_mock.assert_not_called()
