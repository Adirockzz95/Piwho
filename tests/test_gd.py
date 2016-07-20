import unittest
import os
try:
    from gdetect import genderdetect
    CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR_PATH = os.path.join(CURRENT_DIR_PATH, 'data')


    class TestGenderDetect(unittest.TestCase):
        def test_silence_detection(self):
            genderdetect._segmentation(os.path.join(DATA_DIR_PATH,
                                                    'arctic_a0001.wav'))
            self.assertTrue(os.path.isfile('./arctic_a0001.seg'))
            try:
                os.remove('./arctic_a0001.seg')
            except IOError:
                raise

        def test_gen_detection(self):
            genderdetect._segmentation(os.path.join(DATA_DIR_PATH,
                                                    'arctic_a0001.wav'))
            genderdetect._scoring_segments(os.path.join(DATA_DIR_PATH,
                                                        'arctic_a0001.wav'))
            self.assertTrue(os.path.isfile('./arctic_a0001.seg'))
            self.assertTrue(os.path.isfile('./arctic_a0001.g.seg'))
            try:
                os.remove('./arctic_a0001.seg')
                os.remove('./arctic_a0001.g.seg')
            except IOError:
                raise

        def test_gender_identification(self):
            gender = None
            gender = genderdetect.identify_gender(os.path.join(DATA_DIR_PATH,
                                                           'arctic_a0001.wav'))
            self.assertNotEqual(gender, None)
            print (('gender:'+gender))
            try:
                os.remove('./arctic_a0001.seg')
                os.remove('./arctic_a0001.g.seg')
            except IOError:
                raise
except ImportError:
    print ('*** Gender detection module (lium) is not installed'
                     ' skipping test module ***')
