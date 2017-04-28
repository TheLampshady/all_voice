from all_voice.models import AllVoiceUser

from tests.base import TestBaseIntent


class TestUser(TestBaseIntent):

    def setUp(self):
        AllVoiceUser.reset()

    def test_save_error(self):
        message = "Error"
        AllVoiceUser.log_error(1, message)
        resp = AllVoiceUser.get_error(1)
        self.assertEqual(AllVoiceUser._database[1][0], message)

    def test_get_error(self):
        message = "Error"
        AllVoiceUser.log_error(1, message)
        resp = AllVoiceUser.get_error(1)
        self.assertEqual(resp, message)

    def test_reduce_database(self):
        message = "Error"
        for x in range(0, AllVoiceUser._db_limit+5):
            AllVoiceUser.log_error(x, message)
        for x in range(4, -1, -1):
            AllVoiceUser.log_error(x, message)

        self.assertEqual(len(AllVoiceUser._database), AllVoiceUser._db_limit)
        self.assertFalse(AllVoiceUser._database.get(5))
