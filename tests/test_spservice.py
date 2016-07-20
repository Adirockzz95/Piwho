import os
import sys
import unittest
import time


try:
    from piwho import recognition
except ImportError:
    sys.path.insert(0, '../')
    try:
        from piwho import recognition
    except ImportError:
        raise ImportError('package pywho is not installed properly.')


CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'data')


class TestSpeakerService(unittest.TestCase):

    def test_speaker_service_constructor(self):
        recog = recognition.SpeakerService(DATA_DIR_PATH)
        self.assertIsInstance(recog.sprecog, recognition.SpeakerRecognizer)
        self.assertEqual(recog.debug, False)
        self.assertEqual(recog.proc, None)


    def test_feature_option_setting(self):
        recog = recognition.SpeakerService()
        recog.set_feature_option('-lpc -cheb')
        self.assertEqual(recog.sprecog.feature, ' -lpc -cheb ')

    def test_speaker_service_(self):
        recog = recognition.SpeakerService(DATA_DIR_PATH)
        recog.speaker_name = 'Test'
        recog.start_service()
        self.assertTrue(recog.is_alive)
        self.assertTrue(recog.pid)
        time.sleep(3)
        recog.stop_service()
