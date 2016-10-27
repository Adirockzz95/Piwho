import unittest
import os
import sys
import glob

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

print ("[INFO]: Ignore the follwing error message: ERROR:root:No wav file found in path: /dev/null/")

class TestSpeakerRecognition(unittest.TestCase):

    def test_default_constructor(self):
        recog = recognition.SpeakerRecognizer()

        self.assertEqual(recog.dirpath, os.getcwd())
        self.assertEqual(recog.debug, False)
        self.assertEqual(recog.filepath, None)
        self.assertEqual(recog.feature, ' -endp -lpc -cheb')
        self.assertEqual(recog.last_recognized_file, None)
        self.assertEqual(recog.last_trained_file, None)

    def test_directory_as_constructor_argument(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)

        self.assertEqual(recog.dirpath, os.path.abspath(DATA_DIR_PATH))
        self.assertEqual(recog.debug, False)
        self.assertEqual(recog.filepath, None)
        self.assertEqual(recog.feature, ' -endp -lpc -cheb')
        self.assertEqual(recog.last_recognized_file, None)
        self.assertEqual(recog.last_trained_file, None)

    def test_speaker_name(self):
        recog = recognition.SpeakerRecognizer()
        recog.speaker_name = 'Test'
        self.assertEqual(recog.speaker_name, 'Test')

    def test_feature_option(self):
        recog = recognition.SpeakerRecognizer()
        recog.set_feature_option('-lpc -cheb')
        self.assertEqual(recog.feature, ' -lpc -cheb ')

    def test_create_database_entry(self):
        recog = recognition.SpeakerRecognizer()
        recog._create_entry('Test', 'Test.wav')
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_correct_entry_in_databse_file(self):
        recog = recognition.SpeakerRecognizer()
        recog._create_entry('Test', 'ABC.wav')
        entry = '0,Test,ABC.wav|\n'
        with open('./speakers.txt', 'r') as reader:
            self.assertEqual(entry, reader.readline())
        try:
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_get_recently_added_file_in_directory(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        filename = None
        filename = recog.get_recently_added_file()
        self.assertNotEqual(filename, None)

    def test_convert_file_into_8khz(self):
        recog = recognition.SpeakerRecognizer()
        recog._convert_file(os.path.join(DATA_DIR_PATH, 'arctic_a0001.wav'),
                            os.path.join(DATA_DIR_PATH, 'converted.wav'))
        self.assertTrue(os.path.isfile(os.path.join(DATA_DIR_PATH,
                                                    'converted.wav')))
        try:
            os.remove(os.path.join(DATA_DIR_PATH, 'converted.wav'))
        except IOError:
            raise

    def test_is_good_wav_file(self):
        recog = recognition.SpeakerRecognizer()
        filepath = os.path.join(DATA_DIR_PATH, 'arctic_a0001.wav')
        self.assertTrue(recog._is_good_wave(filepath))

    def test_subprocess_function(self):
        recog = recognition.SpeakerRecognizer()
        filename = os.path.join(DATA_DIR_PATH, 'arctic_a0001.wav')
        cmd = 'cp ' + filename + ' ' + os.path.join(DATA_DIR_PATH, 'copy.wav')
        recog._start_subprocess(cmd)
        self.assertTrue(os.path.isfile(os.path.join(DATA_DIR_PATH,
                                                    'copy.wav')))
        try:
            os.remove(os.path.join(DATA_DIR_PATH, 'copy.wav'))
        except IOError:
            raise

    def test_training_with_recently_added_file(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        recog.speaker_name = 'Test'
        recog.train_new_data()
        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_training_with_specified_file(self):
        recog = recognition.SpeakerRecognizer()
        recog.speaker_name = 'Test'
        recog.train_new_data(os.path.join(DATA_DIR_PATH,
                                          'arctic_a0001.wav'))
        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_training_an_entire_folder(self):
        recog = recognition.SpeakerRecognizer()
        recog.speaker_name = 'Test'
        recog.train_new_data(os.path.join(DATA_DIR_PATH))
        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_identify_recently_added_file(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        recog.speaker_name = 'Test'
        recog.train_new_data() 
        recog.last_trained_file = None
        recog.speaker_name = 'Test2'
        recog.train_new_data()
        name = None
        name = recog.identify_speaker()
        self.assertNotEqual(name, None)
        self.assertEqual(name[0], 'Test')
        self.assertEqual(name[1], 'Test2')

    def test_identify_specified_file(self):
        recog = recognition.SpeakerRecognizer()
        name = None
        name = recog.identify_speaker(os.path.join(DATA_DIR_PATH,
                                                   'arctic_a0001.wav'))
        self.assertNotEqual(name, None)
        self.assertEqual(name[0], 'Test')
        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_get_speaker_from_database(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        recog.speaker_name = 'Test'
        recog.train_new_data()

        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        recog.speaker_name = 'Test1'
        recog.train_new_data()
        speakers = []
        speakers = recog.get_speakers()
        self.assertEqual(speakers[0], 'Test')
        self.assertEqual(speakers[1], 'Test1')

        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

    def test_no_speaker_set_exception(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        self.assertRaises(ValueError, recog.train_new_data)

    def test_no_wav_file_found_exception_training(self):
        recog = recognition.SpeakerRecognizer('/dev/null/')
        recog.speaker_name = 'Test'
        self.assertRaises(ValueError, recog.train_new_data)

    def test_no_wav_file_found_exception_identify(self):
        recog = recognition.SpeakerRecognizer('/dev/null/')
        self.assertRaises(IOError, recog.identify_speaker)

    def test_no_speaker_db_found(self):
        recog = recognition.SpeakerRecognizer()
        self.assertRaises(IOError, recog.get_speakers)

    def test_recently_added_file_exception(self):
        recog = recognition.SpeakerRecognizer('/dev/null/')
        self.assertRaises(ValueError, recog.get_recently_added_file)

    def test_speaker_scores(self):
        recog = recognition.SpeakerRecognizer(DATA_DIR_PATH)
        recog.speaker_name = 'Test'
        recog.train_new_data()
        recog.last_trained_file = None
        recog.speaker_name = 'Test2'
        recog.train_new_data(os.path.join(DATA_DIR_PATH,
                                                   'arctic_a0001.wav'))

        recog.identify_speaker()
        dictn = recog.get_speaker_scores()
        self.assertTrue(dictn)
        model = glob.glob('*.gzbin')
        self.assertTrue(os.path.isfile('./' + ''.join(model)))
        self.assertTrue(os.path.isfile('./speakers.txt'))
        try:
            os.remove('./' + ''.join(model))
            os.remove('./speakers.txt')
        except IOError:
            raise

if __name__ == "__main__":
    unittest.main()
