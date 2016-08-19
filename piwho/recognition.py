# -*- coding: utf-8-*-

"""
Module contains speaker training and identification functions
"""
import os
import subprocess
import signal
import glob
import shlex
import time
import logging
import wave
import re
import multiprocessing as mp

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# module to setup data files
from . import config

"""
Terminology:
    MARF internals: corresponds to the internal working and parameters
    of MARF.
    database: speakers.txt
    model : .gzbin file
"""


class SpeakerRecognizer(object):
    """
    This class holds data and functions for speaker training and
    recognition.
    """
    def __init__(self, dirpath=None):
        """
        :type dirpath: string
        :param dirpath: directory path for the wav file.

        """
        #: set current directory as default
        if dirpath is None:
            self.dirpath = os.getcwd()
        else:
            #: get absolute path of directory
            self.dirpath = os.path.abspath(dirpath)

        #: If true then read MARF's stdout and print as it is.
        #: Set True when there's something wrong with the output.
        self.debug = False

        self.last_trained_file = None
        self.last_recognized_file = None

        #: set speaker name for training the model
        self.speaker_name = None

        #: store current filepath
        self.filepath = None

        #: store likehood scores of each speaker
        self.scores = []

        #: set feature for MARF training and recognition
        self.feature = ' -lpc'

    def train_new_data(self, filepath=None, speakername=None):
        """
        Train data with given wav file

        If the filepath is not given then the recently added file
        in directory passed in constructor will be used for training.

        MARF-internals- This will automatically create speakers.txt file
        if is not present.

        :param str filepath: path of the file or directory
         to be trained
        :param str speakername: speakername for the current file
        """
        if speakername is None and self.speaker_name is None:
            raise ValueError('field speaker_name cannot be None.')

        if speakername is None:
            speakername = self.speaker_name

        # If filepath parameter is a directory
        # TODO: buffer filenames and pass it to _create_entry function
        # only once.
        if filepath is not None and os.path.isdir(filepath):
            lists = os.listdir(filepath)
            self.filepath = filepath
            for wav in lists:
                if wav.endswith('.wav'):
                    fullpath = os.path.realpath(
                        os.path.join(self.filepath, wav))

                    # check if wav is suitable for MARF's format
                    if not self._is_good_wave(fullpath):
                        self._convert_file(fullpath)

                    # store file name
                    self.last_trained_file = wav

                    # create entry in the speakers.txt before starting
                    # the training process.
                    self._create_entry(speakername, self.last_trained_file)

            # get result from process
            # start_subprocess returns a list
            reply = self._start_subprocess('java ' + config.JAVA_MEM +
                                           '-jar ' + config.SPEAKER_RECOG_JAR +
                                           ' --train ' + filepath +
                                           self.feature)

        # If filepath parameter is a wav file
        if filepath is not None and os.path.isfile(os.path.abspath(filepath)):
            expand = os.path.expanduser(filepath)
            self.last_trained_file = os.path.basename(expand)

            if not self._is_good_wave(expand):
                self._convert_file(expand)

            self._create_entry(speakername, self.last_trained_file)
            reply = self._start_subprocess('java ' + config.JAVA_MEM +
                                           '-jar ' + config.SPEAKER_RECOG_JAR +
                                           ' --single-train ' + expand +
                                           self.feature)

        # If filepath parameter is not given then
        # use directory path passed in constructor and
        # get recently added file from that directory.
        elif filepath is None:
            expand = os.path.join(self.dirpath, '')
            try:
                newest = max(glob.iglob((expand + '*.wav')),
                             key=os.path.getctime)
            except ValueError:
                logging.error('No wav file found in path: ' + (expand))
                raise

            # do not train same file again
            if self.last_trained_file == os.path.basename(newest):
                return

            elif not self._is_good_wave(newest):
                self._convert_file(newest)

            self.last_trained_file = os.path.basename(newest)
            self._create_entry(speakername, self.last_trained_file)
            reply = self._start_subprocess('java ' + config.JAVA_MEM +
                                           '-jar ' + config.SPEAKER_RECOG_JAR +
                                           ' --single-train ' + newest +
                                           self.feature)

        if self.debug:
            # sanitize string
            data = (''.join(str(x) for x in reply))
            fi = data.encode('ascii', 'ignore').decode('unicode_escape')
            print((re.sub("[b']", '', fi)))

    def identify_speaker(self, audiofile=None):
        """
        Identify the speaker in the audio wav according to speakers.txt
        database and trained model.

        It will always return speaker name from the database as the
        MARF is a closed set framework.

        You can use function 'get_speaker_scores()' to print the
        likehood score for each speaker.

        If the audio filepath is not given then the recently added file
        in the directory 'dirpath' will be used for identification.

        :param str audiofile: audio file for the speaker identification
        :return: the identified speaker
        :Raises: ValueError, IndexError
        """

        # If audiofile is not given then use directory path passed in
        # constructor for extracting the wav file.
        if audiofile is None:

            # add trailing backslash to path
            expand = os.path.join(self.dirpath, '')
            try:
                newest = max(glob.iglob((expand + '*.wav')),
                             key=os.path.getctime)
            except ValueError:
                logging.error('No wav file found in path: ' + expand)
                raise

            if not self._is_good_wave(newest):
                self._convert_file(newest)
            self.last_recognized_file = os.path.basename(newest)
            name = self._start_subprocess('java ' + config.JAVA_MEM +
                                          '-jar ' + config.SPEAKER_RECOG_JAR +
                                          ' --ident ' + newest + self.feature)
            self.scores = name[3:]
            if not self.debug:
                try:
                    return str((name[2].split()[2]).decode('utf-8'))
                except IndexError:
                    logging.error('MARF execution failed.'
                                  ' Please set debug=True to print error'
                                  ' info.', exc_info=True)

            else:
                # sanitize string
                data = (''.join(str(x) for x in name))
                fi = data.encode('ascii', 'ignore').decode('unicode_escape')
                print((re.sub("[b']", '', fi)))

        # if audiofile is passed
        else:
            expand = os.path.expanduser(audiofile)

            if not self._is_good_wave(expand):
                self._convert_file(expand)
            # handle this error
            name = self._start_subprocess('java ' + config.JAVA_MEM +
                                          '-jar ' + config.SPEAKER_RECOG_JAR +
                                          ' --ident ' + expand + self.feature)

            self.scores = name[3:]
            if not self.debug:
                try:
                    return str((name[2].split()[2]).decode('utf-8'))
                except IndexError:
                    logging.error('MARF execution failed.'
                                  ' Please set debug=True to print error'
                                  ' info.', exc_info=True)

            else:
                data = (''.join(str(x) for x in name))
                fi = data.encode('ascii', 'ignore').decode('unicode_escape')
                print((re.sub("[b']", '', fi)))


    def get_speaker_scores(self):
        """
        Returns a dictonary of speakers and their respective distances.

        get stored score values from 'self.scores' and
        split them into a list. get speaker list from
        database and combine each speaker with it's score value.

        These scores represents the distance of recognized audio file
        to the speakers from databse.

        Minimum the distance closer the speaker to the recognized file.

        :return: a dictionary
        :rtype: dict
        """
        strs = [str(self.scores[i]).strip().split(":")[1].replace("\\n'","")
                for i, x in enumerate(self.scores)]

        names = self.get_speakers()
        dictn = {index: v for index, v in zip(names, strs)}
        return dictn

    def get_speakers(self):
        """
        Parse speakers.txt file to get speaker names and return a list.

        :return: speaker list from database
        :raises: IOError
        """
        try:
            with open(config.SPEAKER_DB, 'r') as reader:
                speakers = [row.split(',')[1] for row in reader]
            return speakers
        except IOError:
            raise

    def _create_entry(self, speakername, filename):
        """
        Update the speakers.txt for each new audio file.
        Create speakers.txt if not exist.

        Find speakername in the file, if found, appends filename
        at the end of it otherwise create a new entry.

        :param str speakername: speaker name for training
        :param str filename: filename of audio file.
        :raises: IOError
        """
        # check if speakers.txt exists and if not create
        # an empty file.
        if not os.path.isfile(config.SPEAKER_DB):
            try:
                open(config.SPEAKER_DB, 'w').close()
            except IOError:
                raise

        with open(config.SPEAKER_DB, 'r') as reader:
            with open('speakers.tmp', 'w+') as writer:
                found = False

                # if speaker is present in speakers.txt
                # go at the end of last entry and append
                # new file name.
                for row in reader:
                    if speakername in row:
                        line = row.rstrip('\n')
                        line += filename + '|'
                        writer.write(line + '\n')
                        found = True
                    else:
                        writer.write(row)

                    lastline = row

                # if speaker is not present in speakers.txt
                if not found:

                    # check if this is the first entry in the file
                    if os.stat(config.SPEAKER_DB).st_size == 0:
                        curr_id = '0'

                    # if not then append new entry at the end of the file
                    # new entry format : ID,speakername,filename|
                    else:
                        curr_id = chr(ord(lastline[0][0]) + 1)
                    new_entry = (curr_id + ',' + speakername +
                                 ',' + filename + '|')
                    writer.write(new_entry + '\n')

        os.remove(config.SPEAKER_DB)
        os.rename('speakers.tmp', config.SPEAKER_DB)
        reader.close()
        writer.close()

    def get_recently_added_file(self):
        """
        return recently added filename from the directory
        passed in constructor.

        :return: directory path of the file
        :rtype: string
        :raises: ValueError
        """
        expand = os.path.join((os.path.expanduser(self.dirpath)), '')
        try:
            newest = max(glob.iglob((expand + '*.wav')),
                         key=os.path.getctime)
            return newest
        except ValueError:
            logging.error('No wav file found in path: ' + expand)
            raise

    def set_feature_option(self, feature=None):
        """
        set feature Extraction option for MARF
        """
        if feature is not None:
            self.feature = ''.join([' ',feature,' '])

    def _convert_file(self, src, dest=None):
        """
        convert wav into 8khz rate
        """
        if dest is None:
            temp = src + '.temp'
            os.rename(src, temp)
            self._start_subprocess('sox ' + temp + ' -r 8000 ' + src)
            os.remove(temp)
        else:
            self._start_subprocess('sox ' + src + ' -r 8000 ' + dest)

    def _is_good_wave(self, filename):
        """
        check if wav is in correct format for MARF.
        """
        par = None
        try:
            w_file = wave.open(filename)
            par = w_file.getparams()
            w_file.close()
        except wave.Error as exc:
            print (exc)
            return False

        if par[:3] == (1, 2, 8000) and par[-1:] == ('not compressed',):
            return True
        else:
            return False

    def _start_subprocess(self, commandline):
        """
        Start a subprocess with the given commandline and wait for
        termination.

        :param str commandline: commandline string
        :return: output from stdout, stderr
        :rtype: list
        """
        args = shlex.split(commandline)
        procs = subprocess.Popen(args, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        # always read stdout
        sout = procs.stdout.readlines()

        if self.debug:
            # read stderr only when debugging is required
            serr = procs.stderr.readlines()
            procs.wait()
            # add two lists and return
            return serr + sout
        else:
            procs.wait()
            return sout


    def marf_feature_options(self):
        """
        Print MARF feature options which can be used for speaker training
        and recognition.
        """
        features = """

        Options (one or more of the following):

        Preprocessing:

            -raw          - no preprocessing
            -norm         - use just normalization, no filtering
            -low          - use low-pass filter
            -high         - use high-pass filter
            -boost        - use high-frequency-boost preprocessor
            -band         - use band-pass filter

        Feature Extraction:

            -lpc          - use LPC
            -fft          - use FFT
            -minmax       - use Min/Max Amplitudes
            -randfe       - use random feature extraction

        Classification:

            -cheb         - use Chebyshev Distance
            -eucl         - use Euclidean Distance
            -mink         - use Minkowski Distance
            -diff         - use Diff-Distance
            -randcl       - use random classification

        Use set_feature_option() to use any of these features.
        Example: set_feature_options('-norm -lpc -cheb')
        Changing options will affect the recognition accuracy.
        See marf Manual:
        http://marf.sourceforge.net/docs/marf/0.3.0.5/report.pdf    """
        print(features)


class SpeakerService(FileSystemEventHandler):

    """
    Class that creates a background service to train model automatically.
    """

    def __init__(self, dirpath=None):
        """
        Invokes the SpeakerRecognizer constructor with params.

        :type: dirpath: string
        :param: path for the .wav file
        """
        self.proc = None
        self.sprecog = SpeakerRecognizer(dirpath)
        self.event = mp.Event()
        self.debug = False
        self.speaker_name = None

    def __run(self, event):
        """
        Create watchdog Observer object and start service
        """
        obsrv = Observer()
        obsrv.schedule(self, path=self.sprecog.dirpath, recursive=False)
        obsrv.start()
        event.wait()

        if event.is_set():
            obsrv.stop()
            obsrv.join()

    def start_service(self):
        """
        start speaker training service.
        """
        # prevent signal from propagating to child process
        handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        if self.debug:
            self.sprecog.debug = True
            mp.log_to_stderr(logging.DEBUG)

        self.sprecog.speaker_name = self.speaker_name
        self.proc = mp.Process(name="watchdog", target=self.__run,
                               args=(self.event,))
        self.proc.setDaemon = False
        self.proc.start()
        # restore signal
        signal.signal(signal.SIGINT, handler)

    def stop_service(self):
        """
        stop speaker training service
        """
        # tell child process to stop
        self.event.set()
        time.sleep(0.5)
        # join parent process
        self.proc.join()

    @property
    def pid(self):
        """
        return pid of current process
        """
        return self.proc.pid

    @property
    def is_alive(self):
        """
        check if current process is alive
        """
        return self.proc.is_alive()

    def on_created(self, event):
        """
        This method will be called on every
        FileCreateEvent of watchdog
        """
        self.sprecog.train_new_data()

    def set_feature_option(self, feature=None):
        """
        set feature Extraction method for MARF
        """
        if feature is not None:
            self.sprecog.feature = ''.join([' ', feature, ' '])
