import requests
import time

LIFX_TOKEN = "cad3571b1401ca1974e34d12b34bd2dfcb14e8d440b17b5494a5b7f300df40c2"

headers= {"Authorization":"Bearer %s" % LIFX_TOKEN}

response = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)

lights = response.json()

for light in lights:
    print(light['label'])
    if "Room 2" in light['label']:
        leftLight = light
        mylight = light
    if "Room  1" in light['label']:
        rightLight = light

print("%s: %s" % (mylight['label'], mylight['id']))
urlStateTv  = 'https://api.lifx.com/v1/lights/location_id:%s/state' % mylight['location']['id']
urlStateTv2 = 'https://api.lifx.com/v1/lights/id:%s/state' % mylight['id']
urlStateTvLeft = 'https://api.lifx.com/v1/lights/id:%s/state' % leftLight['id']
urlStateTvRight = 'https://api.lifx.com/v1/lights/id:%s/state' % rightLight['id']
urlStrobeTv = 'https://api.lifx.com/v1/lights/all/effects/pulse'

def goRed(url):
    print("red")
    data = {
        'color':'red',
        'duration':0,
    }
    response = requests.put(url, data=data, headers=headers)

def goBlue(url):
    print("blue")
    data = {
        'color':'blue',
        'duration':0,
    }
    response = requests.put(url, data=data, headers=headers)

def go3500():
    print("kelvin:3500")
    data = {
        'color':'kelvin:3500 brightness:1.0',
        'duration':3,
    }
    response = requests.put(urlStateTv, data=data, headers=headers)
    time.sleep(3)

def strobe():
    print("strobe")
    data = {
        'period':1,
        'cycles':6,
        'color':'brightness:0.15'
    }
    print(urlStrobeTv)
    response = requests.post(urlStrobeTv, data=data, headers=headers)
    print(response)

go3500()

goBlue(urlStateTvLeft)
goRed(urlStateTvRight)
goRed(urlStateTvLeft)
goBlue(urlStateTvRight)

goBlue(urlStateTvLeft)
goRed(urlStateTvRight)
goRed(urlStateTvLeft)
goBlue(urlStateTvRight)

goBlue(urlStateTvLeft)
goRed(urlStateTvRight)
goRed(urlStateTvLeft)
goBlue(urlStateTvRight)

go3500()
