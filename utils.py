#!env/bin/python3
from datetime import datetime

def getCurrentDayTime():
  return (datetime.today()).strftime('%Y-%m-%d_%Hh%Mm%Ss')


def saveData(save_path, fileName, dataToSave):
  with open(save_path + fileName, 'w') as data_file:
    data_file.write(dataToSave)
