#!env/bin/python3
import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("config.ini")


def getAllPollutionData():
  token = config['AQICN']['TOKEN']
  site = config['AQICN']['FEED_SENSOR']
  URL = "https://api.waqi.info/feed/@" + site + "/?token=" + token
  all_data_json = json.loads(requests.get(URL).text)

  all_data_dict = {}
  all_data_dict['dominentpol'] = all_data_json['data']['dominentpol']
  for data_pt in all_data_json['data']['iaqi']:
    all_data_dict[data_pt] = round(all_data_json['data']['iaqi'][data_pt]['v'])
  return all_data_dict


def getCurrentPollutionIndex():
  current_status = getAllPollutionData()
  dominant_pollutant = current_status['dominentpol']
  return str(current_status[dominant_pollutant])


def getPollutionData(data_point):
  return str(getAllPollutionData()[data_point])
