import bottle
import json
import serial

SERIAL = serial.Serial("COM3", 9600)
CONFIG_PATH = "./.sha.config"

@bottle.route('/hello/<name>')
def index(name):
    return bottle.template('<b>Hello {{name}}</b>!', name=name)

@bottle.route('/set/receiver/source/am')
def setAudioSourceAm():
    print("Setting audio source to AM Radio.")
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::am"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/amfm')
def setAudioSourceAm():
    print("Setting audio source to AM/FM Radio.")
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::am"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/cd')
def setAudioSourceCd():
    print("Setting audio source to CD Player.")
    SERIAL.write(b":rincd:")
    confirmation = [{"success": 1, "request": "set::receiver::source::cd"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/entsys')
def setAudioSourceEntSys():
    print("Setting audio source to Entertainment System.")
    SERIAL.write(b":rinmulti:")
    confirmation = [{"success": 1, "request": "set::receiver::source::entsys"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/fm')
def setAudioSourceFm():
    print("Setting audio source to FM Radio.")
    SERIAL.write(b":rintuner:")
    confirmation = [{"success": 1, "request": "set::receiver::source::fm"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/laptop')
def setAudioSourceLaptop():
    print("Setting audio source to Laptop (Jolteon).")
    SERIAL.write(b":rinvcr:")
    confirmation = [{"success": 1, "request": "set::receiver::source::laptop"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/pc')
def setAudioSourcePc():
    print("Setting audio source to PC (Carterpie).")
    SERIAL.write(b":rincbl:")
    confirmation = [{"success": 1, "request": "set::receiver::source::pc"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/turntable')
def setAudioSourceTurntable():
    print("Setting audio source to Turntable.")
    SERIAL.write(b":rintape:")
    confirmation = [{"success": 1, "request": "set::receiver::source::turntable"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

@bottle.route('/set/receiver/source/xm')
def setAudioSourceXm():
    print("Setting audio source to XM Radio.")
    SERIAL.write(b":rinaux:")
    confirmation = [{"success": 1, "request": "set::receiver::source::xm"}]
    bottle.response.content_type = 'application/json'
    return json.dumps(confirmation)

class ShaConfig(object):
    def __init__(self):
        global CONFIG_PATH
        if not os.path.exists(CONFIG_PATH):
            self.setToDefailt()

    def setToDefault(self):
        defaults = {
            audioIn = "xm",
            audioOuts = [],
            audioPresets = [],
            lightScenes = []
        }
        with open(CONFIG_PATH, "w") as fh:
            fh.write({})


if __name__ == "__main__":
    shaConfig = ShaConfig()
    bottle.run(host='localhost', port=8082)
