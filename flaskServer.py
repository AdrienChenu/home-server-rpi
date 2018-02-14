import json
from urllib.request import urlopen as urlRequestOpen
from urllib.parse import quote
import configparser
from flask import Flask
from flask import jsonify
import TFL
import aqicn
import utils

config = configparser.ConfigParser()
config.read("config.ini")

KAROTZ_IP = config['KAROTZ']['IP_ADDRESS']
BASE_RABBIT_URL = 'http://' + KAROTZ_IP + '/cgi-bin/tts?voice=7&nocache=0&text='

app = Flask(__name__)


@app.route("/tfl", methods=['GET'])
@app.route("/tfl/status", methods=['GET'])
def getAllLineStatus():
  TFL.getXMLStatus()
  return str(TFL.summarizeStatusAllLines())


@app.route('/tfl/<LineName>')
def getLineStatus(LineName):
  TFL.getXMLStatus()
  status = "There is " \
           + str(TFL.getLineStatus(LineName)[0]) \
           + " on the " + LineName + " line. " \
           + str(TFL.getLineStatus(LineName)[1])
  return status


@app.route('/tfl/askRabbit/<LineName>', methods=['GET'])
def getRabbitToTellTflStatus(LineName):
  TFL.getXMLStatus()
  #quote: url encoding
  if LineName == "status":
    msg = quote(TFL.summarizeStatusAllLines())
  else:
    msg = quote("There is "
                + str(TFL.getLineStatus(LineName)[0])
                + " on the " + LineName + " line")

  urlRequestOpen(BASE_RABBIT_URL + msg)
  return BASE_RABBIT_URL + msg


@app.route('/aqicn/pollutionIndex', methods=['GET'])
def getCurrentPollutionIndex():
  return aqicn.getCurrentPollutionIndex()


@app.route('/aqicn/askRabbit/pollutionIndex', methods=['GET'])
def getRabbitToTellPollution():
  msg = quote("The pollution this morning is "
              + str(aqicn.getCurrentPollutionIndex()))
  urlRequestOpen(BASE_RABBIT_URL + msg)
  return BASE_RABBIT_URL + msg


@app.route('/aqicn/SavePollutionData', methods=['GET'])
def saveCurrentPollutionData():
  response = aqicn.getAllPollutionData()
  save_path = config['AQICN']['SAVE_PATH']
  utils.saveData(save_path,
                 "aqicn_index_" + utils.getCurrentDayTime() + ".json",
                 json.dumps(response, sort_keys=False, indent=2))
  return jsonify(response)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
