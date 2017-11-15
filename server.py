#==============================================================================
# Imports
#==============================================================================
import bottle
from bottle import request, abort
import json
import os
import requests
import serial
from threading import Thread

#==============================================================================
# Globals
#==============================================================================
with open('c:/Users/allen/lifxToken.txt', 'r') as fh:
    _token = fh.read()
LIFX_TOKEN = _token.strip()

CONFIG_PATH = "./.sha.config"
HEADERS = {"Authorization": "Bearer %s" % LIFX_TOKEN}
HOME_LOCATION = "Grammy"
SHA_CONFIG = None

try:
    SERIAL = serial.Serial("COM3", 9600)
except serial.serialutil.SerialException:
    print("WARNING: No Serial device connected.")
    SERIAL = None
'''
response = requests.get('https://api.lifx.com/v1/lights/all', headers=HEADERS)
lights = response.json()

for light in lights:
    print(light['label'])
    if "Room 2" in light['label']:
        leftLight = light
        mylight = light
    if "Room  1" in light['label']:
        rightLight = light
'''

#==============================================================================
# Routes
#==============================================================================
@bottle.route('/hello/<name>')
def index(name):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)

#------------------------------------------------------------------------------
# Lights
#------------------------------------------------------------------------------
#____ Getters ____
@bottle.route('/get/lifx/lights/all')
def getLifxLightsAll():
    global SHA_CONFIG
    bottle.response.content_type = 'application/json'
    return json.dumps(SHA_CONFIG.get("lights"))

@bottle.route('/get/lifx/lights/id/<lightId>')
def getLifxLightsById(lightId):
    #urlQuery = 'https://api.lifx.com/v1/lights/id:{}'.format(lightId)
    for light in getLifxLightsAll():
        if light['id'] == lightId:
            return json.dumps(light)

@bottle.route('/get/lifx/location')
def getLifxLocation():
    bottle.response.content_type = 'application/json'
    return json.dumps(SHA_CONFIG.get("location"))

@bottle.route('/get/lifx/scenes')
def getLifxScenes():
    global SHA_CONFIG
    bottle.response.content_type = 'application/json'
    return json.dumps(SHA_CONFIG.get("scenes"))

#____ Setters ____
@bottle.route('/set/lifx/lights/id:<lightId>/state', method='PUT')
def setLifxLightState(lightId):
    data = dict(request.params)
    if not data:
        abort(422, "Missing data parameter")
    url = 'https://api.lifx.com/v1/lights/id:%s/state' % id
    response = requests.put(url, data=data, headers=HEADERS)
    return response

@bottle.route('/set/lifx/location/state', method='POST')
def setLifxLocationState():
    data = request.query.data
    url = 'https://api.lifx.com/v1/lights/location:{}/state'.format(HOME_LOCATION)
    response = requests.put(url, data=data, headers=HEADERS)
    return response


#------------------------------------------------------------------------------
# Audio
#------------------------------------------------------------------------------
#____ Getters ____
@bottle.route('/get/receiver/power')
def getReceiverPower():
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    #MAINT: Add success logic

@bottle.route('/get/receiver/source')
def getReceiverPower():
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    #MAINT: Add success logic

#____ Setters ____
@bottle.route('/set/receiver/source/am')
def setAudioSourceAm():
    print("Setting audio source to AM Radio.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::am"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/amfm')
def setAudioSourceAm():
    print("Setting audio source to AM/FM Radio.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::am"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/cd')
def setAudioSourceCd():
    print("Setting audio source to CD Player.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rincd:")
    confirmation = [{"success": 1, "request": "set::receiver::source::cd"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/entsys')
def setAudioSourceEntSys():
    print("Setting audio source to Entertainment System.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rinmulti:")
    confirmation = [{"success": 1, "request": "set::receiver::source::entsys"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/fm')
def setAudioSourceFm():
    print("Setting audio source to FM Radio.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::fm"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/laptop')
def setAudioSourceLaptop():
    print("Setting audio source to Laptop (Jolteon).")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rinvcr:")
    confirmation = [{"success": 1, "request": "set::receiver::source::laptop"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/pc')
def setAudioSourcePc():
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    print("Setting audio source to PC (Carterpie).")
    SERIAL.write(b":rincbl:")
    confirmation = [{"success": 1, "request": "set::receiver::source::pc"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/turntable')
def setAudioSourceTurntable():
    print("Setting audio source to Turntable.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rintape:")
    confirmation = [{"success": 1, "request": "set::receiver::source::turntable"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/xm')
def setAudioSourceXm():
    print("Setting audio source to XM Radio.")
    if not SERIAL:
        confirmation = [{"success": 0}]
        bottle.response.content_type = 'application/json'
        return json.dumps(confirmation)
    SERIAL.write(b":rinaux:")
    confirmation = [{"success": 1, "request": "set::receiver::source::xm"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

def updateShaConfig():
    global SHA_CONFIG
    lights = requests.get('https://api.lifx.com/v1/lights/all', headers=HEADERS)
    scenes = requests.get('https://api.lifx.com/v1/scenes', headers=HEADERS)
    urlQuery = 'https://api.lifx.com/v1/lights/location:' + HOME_LOCATION
    location = requests.get(urlQuery, headers=HEADERS)
    #print("ALLEN lights:\n{} {}\n{}\n\n".format(lights, type(lights), lights.json()))
    #print("ALLEN scenes:\n{} {}\n{}\n\n".format(scenes, type(scenes), scenes.json()))
    if not lights.ok and scenes.ok and location.ok:
        raise(NetworkError,
              "Failed to retrieve LIFX data from network:\n{}\n{}\n{}".format(lights, scenes, location))
    SHA_CONFIG.set("lights", lights.json())
    SHA_CONFIG.set("scenes", scenes.json())
    SHA_CONFIG.set("location", scenes.json())
    SHA_CONFIG.writeData()

#==============================================================================
# Classes
#==============================================================================
class NetworkError(RuntimeError):
    def __init__(self, args):
        self.args = args

class ShaConfig(object):
    def __init__(self):
        global CONFIG_PATH
        if not os.path.exists(CONFIG_PATH):
            self.setToDefault()
        else:
            self.data = self.readData()

    def setToDefault(self):
        defaults = {
            'audioIn': "xm",
            'audioOuts': [],
            'audioPresets': [],
            'lightScenes': []
        }
        self.data = defaults
        with open(CONFIG_PATH, "w") as fh:
            fh.write(json.dumps(defaults))

    def readData(self):
        with open(CONFIG_PATH, "r") as fh:
            data = json.loads(fh.read())
        return data

    def writeData(self):
        with open(CONFIG_PATH, "w") as fh:
            fh.write(json.dumps(self.data))

    def get(self, attr):
        if not attr in self.data:
            return None
        else:
            return self.data[attr]

    def set(self, attr, value):
        self.data[attr] = value



#==============================================================================
# Main
#==============================================================================
if __name__ == "__main__":
    SHA_CONFIG = ShaConfig()
    updateShaConfig()
    bottle.run(host='localhost', port=8082)
