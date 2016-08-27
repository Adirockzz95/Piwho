import os

__VERSION__ = '1.1.0'

JAR_PATH = 'marf'
MARF_DEFAULT = os.path.join(os.path.dirname(__file__), JAR_PATH,
                            './marf.jar')

SPEAKER_RECOG_JAR = os.path.join(os.path.dirname(__file__), JAR_PATH,
                                 './Speaker.jar')
# Do not change SPEAKER_DB
SPEAKER_DB = './speakers.txt'

JAVA_MEM = '-Xmx100m '
