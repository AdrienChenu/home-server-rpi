#!env/bin/python3
from xml.dom import minidom
from urllib.request import urlopen as urlRequestOpen

url_tfl_linestatus = 'http://cloud.tfl.gov.uk/TrackerNet/LineStatus'

def getXMLStatus():
  global xmldoc  # pylint: disable=W0601
  xmldoc = minidom.parse(urlRequestOpen(url_tfl_linestatus))


def __getNameFromLineStatusObject(lineStatus):
  return lineStatus.getElementsByTagName('Line')[0].attributes['Name'].value


def __getStatusDescriptionFromLineStatusObject(lineStatus):
  return lineStatus.getElementsByTagName('Status')[0].attributes['Description'].value


def __getStatusDetailsFromLineStatusObject(lineStatus):
  # if PYTHON2 put item(0), if PYTHON3 put item(1)... no comment
  return str(lineStatus.attributes['StatusDetails'].value)


def getLineStatus(name):
  # in: xml of the line statuses, name of the line searched
  # out: line status description

  # initialise loop
  lineStatusList = xmldoc.getElementsByTagName('LineStatus')
  count = 0
  lineStatus = lineStatusList[count]
  lineName = __getNameFromLineStatusObject(lineStatus)

  # run loop until name is found or last item in list
  while lineName.lower() != name.lower() and count + 1 < lineStatusList.length:
    lineStatus = lineStatusList[count + 1]
    count = count + 1
    lineName = __getNameFromLineStatusObject(lineStatus)

  if lineName.lower() == name.lower():
    return (__getStatusDescriptionFromLineStatusObject(lineStatus),
            __getStatusDetailsFromLineStatusObject(lineStatus))
  else:
    return "Status for line '" + name + "' not found."


def getAllLinesNames():
  # in: xmls of the line statuses
  # out: list of line names
  lineStatusList = xmldoc.getElementsByTagName('LineStatus')
  lineList = []
  for s in lineStatusList:
    lineList.append(__getNameFromLineStatusObject(s))
  return lineList


def getAllLinesStatus():
  statusList = []
  for l in getAllLinesNames():
    statusList.append(getLineStatus(l))
  return statusList


def summarizeStatusAllLines():
  # function getAllLinesStatus returns a tupple
  # with the line status as 1st element
  # with the description for the delay as 2nd element
  lineStatus = [getAllLinesNames(), [x[0] for x in getAllLinesStatus()],
                [x[1] for x in getAllLinesStatus()]]
  msg = ""
  msg_reason_delays = ""
  for i in range(0, len(lineStatus[0])):
    l = lineStatus[0][i]  # line name
    s = lineStatus[1][i]  # line status
    r = lineStatus[2][i]  # reason for delay

    if s != "Good Service":
      msg = msg + s + " on the " + l + " line, "
      msg_reason_delays = msg_reason_delays + " " + l + " line: " + r

  if msg != "":
    msg = "There is " + msg + ". Good service on all other lines."
    # comment out next line if you do not want the reason for the delay
    msg = msg + msg_reason_delays
  else:
    msg = "There is good service on all London underground lines"

  return msg

getXMLStatus()
