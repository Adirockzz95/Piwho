Getting started
===============

`Jasper <https://jasperproject.github.io/>`__ is a voice computing
platfrom for Raspberry pi. By integrating piwho with jasper you can:

-  Write user specific modules
-  Play user specific playlists
-  Add speaker recognition to your Pi projects

Prerequisites
-------------

-  Pi 1 / Pi 2 / Pi 3 (not tested)
-  working copy of jasper's
   `master <https://github.com/jasperproject/jasper-client/tree/master>`__
   or
   `dev <https://github.com/jasperproject/jasper-client/tree/jasper-dev>`__
   branch
-  `piwho <https://www.github.com/Adirockzz95/piwho>`__ library
   installed

**Note:** Take a backup of your jasper project.

configuring jasper:
-------------------

The following changes will extract the recordings from jasper.

-  **If you're using master branch:**

create a new directory inside jasper :

.. code:: bash

    $ cd ~/jasper/
    $ mkdir recordings

open ``/jasper/client/mic.py`` and add the following imports:

.. code:: python

    import time
    import datetime
    import shutil
    import os

go to end of the file and add this function:

.. code:: python

    def gettime(self):
        current = time.time()
        tformat = datetime.datetime.fromtimestamp(current).strftime('%d:%H:%M:%S')
        return tformat

find function ``activeListenToAllOptions()`` and in that function
comment out the following code:

.. code:: python

    with tempfile.SpooledTemporaryFile(mode='w+b') as f:
        wav_fp = wave.open(f, 'wb')
        wav_fp.setnchannels(1)
        wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wav_fp.setframerate(RATE)
        wav_fp.writeframes(''.join(frames))
        wav_fp.close()
        f.seek(0)
        return self.active_stt_engine.transcribe(f)

and add the following code:

.. code:: python

    with tempfile.NamedTemporaryFile(mode='w+b') as f:
        wav_fp = wave.open(f, 'wb')
        wav_fp.setnchannels(1)
        wav_fp.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wav_fp.setframerate(RATE)
        wav_fp.writeframes(''.join(frames))
        wav_fp.close()
        f.seek(0)
        # gettime() function will replace temp file name with a timestamp
        path = os.path.join('~/jasper/recordings', (self.gettime() + '.wav'))
         # this will paste recorded file into your recordings folder
        shutil.copyfile(f.name, path)
        return self.active_stt_engine.transcribe(f)

save the file, run Jasper and execute any module. You should see a
``.wav`` file inside ``recordings`` folder. Now you're ready to use
recognition library with jasper.

-  **If you're using dev branch:**

create a new directory inside jasper-client:

.. code:: bash

    $ cd ~/jasper-client/
    $ mkdir recordings

open ``jasper-client/jasper/mic.py`` and add the following imports:

.. code:: python

    import time
    import datetime
    import shutil
    import os

go to end of the file and add this function:

.. code:: python

    def gettime(self):
        current = time.time()
        tformat = datetime.datetime.fromtimestamp(current).strftime('%d:%H:%M:%S')
        return tformat

then in ``_write_frames_to_file(self, frames)`` function:

.. code:: python

    @contextlib.contextmanager
       def _write_frames_to_file(self, frames):
           with tempfile.NamedTemporaryFile(mode='w+b') as f:
               wav_fp = wave.open(f, 'wb')
               wav_fp.setnchannels(self._input_channels)
               wav_fp.setsampwidth(int(self._input_bits/8))
               wav_fp.setframerate(self._input_rate)
               wav_fp.writeframes(''.join(frames))
               wav_fp.close()
               f.seek(0)
               yield f

after ``f.seek(0)`` add the following code:

.. code:: python

        # gettime() function will replace temp file name with a timestamp
        path = os.path.join('~/jasper/recordings', (self.gettime() + '.wav'))
        # this will paste recorded file into your recordings folder
        shutil.copyfile(f.name, path)

save the file, run Jasper and execute any module. You should see a
``.wav`` file inside ``recordings`` folder. Now you're ready to use
recognition library with jasper.

Modules
-----------

See ``examples/jasper/`` directory
