Gender Detection
----------------

You can use
`genderdetect <https://www.github.com/Adirockzz95/GenderDetect.git>`__
module in conjunction with Piwho.

clone github repository

::

    $ git clone https://www.github.com/Adirockzz95/GenderDetect.git
    $ cd genderdetect
    $ python setup.py install

Combine gender detection with speaker recognition:

.. code:: python

    >> from piwho import recognition
    >> from gdetect import genderdetect as gd
    >> # use file from current directory
    >> recog = recognition.SpeakerRecognizer()
    >> # recognize speaker
    >> name = [] 
    >> name = recog.identify_speaker()
    >> # pass the same audio file for gender detection
    >> gender = gd.identify_gender(recog.get_recently_added_file())
    >> print name[0] + ':' + gender
