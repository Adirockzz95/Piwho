* **Module:** recognition
* **class:** SpeakerRecognizer

Module contains speaker training and identification functions

**piwho.recognition.SpeakerRecognizer(dirpath=None)**

Bases: ``object``

| This class holds data and functions for speaker training and
  recognition.

**_convert_file(src, dest=None)**

convert wav into 8khz rate

**_create_entry(speakername, filename)**

| Update the speakers.txt for each new audio file. Create
  speakers.txt if not exist.

| Find speakername in the file, if found, append filename at the
  end of it otherwise create a new entry.

**Parameters:**
 * **speakername** (*str*) -- speaker name for training
 * **filename** (*str*) -- filename of audio file.

**Raises:**
 * IOError

**_is_good_wave(filename)**

check if wav is in correct format for MARF.


**_start_subprocess(commandline)**

Start a subprocess with the given commandline and wait for
termination.

**Parameters:**
 * **commandline** (*str*) -- commandline string

**Returns:**
  output from stdout, stderr

**Return type:** list


**get_recently_added_file()**

 Return recently added filename from the directory passed in
 constructor.

**:Returns:**
  directory path of the file

**Return type:**
  string

**Raises:**
  ValueError

   **get_speaker_scores()**

   |   Returns a dictonary of speakers and their respective distances.

   |   get stored score values from 'self.scores' and split them into a
      list. get speaker list from database and combine each speaker
      with it's score value.

   |   These scores represents the distance of recognized audio file to
      the speakers from databse.

   |   Minimum the distance closer the speaker to the recognized file.

      :Returns:
         a dictionary

      :Return type:
         dict

   **get_speakers()**
    
   |   Parse speakers.txt file to get speaker names and return a list.

      :Returns:
         speaker list from database

      :Raises:
         IOError

   **identify_speaker(audiofile=None)**
   
   |   Identify the speaker in the audio wav according to speakers.txt
      database and trained model.

   |   It will always return speaker name from the database as the MARF
      is closed set framework.

   |   You can use function 'get_speaker_scores()' to print the
      likehood score for each speaker.

   |   If the audio filepath is not given then the recently added file
      from the directory path passed in constructor will be used for identification.

      :Parameters:
         **audiofile** (*str*) -- audio file for the speaker
         identification

      :Returns:
         the identified speaker

      :Raises:
         ValueError, IndexError

   **marf_feature_options()**

   |   Print MARF feature options which can be used for speaker
      training and recognition.

   **set_feature_option(feature=None)**

   |   set feature Extraction option for MARF

   **train_new_data(filepath=None, speakername=None)**

   |   Train data with given wav file

   |   If the filepath is not given then the recently added file from the
      directory path passed in constructor will be used for training.

   |   MARF-internals- This will automatically create speakers.txt file
      if is not present.

      :Parameters:
         * **filepath** (*str*) -- path of the file or directory to be
           trained

         * **speakername** (*str*) -- speakername for the current file


