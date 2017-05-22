import unittest

from all_voice.tests.utils import AllVoiceTestUtils


class TestBaseIntent(AllVoiceTestUtils, unittest.TestCase):

    def setUp(self):
        super(TestBaseIntent, self).setUp()
