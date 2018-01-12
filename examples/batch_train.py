
import os
from piwho import recognition

speakers = ['Aditya','Ankit','Abhishek','Abhinav','Rishi','Mansi','Shivangi','Devika','Kranti']

data_folders = ['sp_Aditya','sp_Ankit','sp_Abhishek','sp_Abhinav','sp_Rishi','sp_Mansi','sp_Shivangi','sp_Devika','sp_Kranti']

folder_path = '/home/pi/train_data/'

def train():
    recog = recognition.SpeakerRecognizer()
    recog.debug = True
    for i in range(len(speakers)):
        recog.speaker_name = speakers[i]
        path =  os.path.join(folder_path,data_folders[i])
        print("speaker name: {} speaker_data: {}".format(speakers[i], data_folders[i]))
        recog.train_new_data(path)

if __name__ == "__main__":
    train()
