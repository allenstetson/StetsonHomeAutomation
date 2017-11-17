# =============================================================================
# Imports
#  =============================================================================
# stdlib
import json
import os
import sys

# Kivy imports
import kivy
kivy.require ('1.10.0')

#Widgets
from kivy.uix.label import Label


# =============================================================================
# Globals
# =============================================================================
STATUS_BAR = Label(text="Problem detected.", size_hint=(1, .1))
WEBROOT = "http://localhost:8082/"
LOCAL_CONFIG_PATH = ".shaLocalConfig"

# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================
class ShaLocalConfig(object):
    def __init__(self):
        global LOCAL_CONFIG_PATH
        self.configPath = LOCAL_CONFIG_PATH
        self.data = {}
        self.getOrCreateConfig()

    def getOrCreateConfig(self):
        if not os.path.exists(self.configPath):
            settings = self.generateDefaults()
            self.data = settings
            self.write()
        else:
            self.read()

    def read(self):
        with open(self.configPath, 'r') as fh:
            self.data = json.loads(fh.read())

    def write(self):
        with open(self.configPath, 'w') as fh:
            fh.write(json.dumps(self.data))

    def generateDefaults(self):
        data = {
            'alarms': {
                'audible': True,
                'led': False,
                'visual': True
            },
            'panes': {
                'audio': True,
                'audio:presets': True,
                'audio:inputs': True,
                'audio:outputs': True,
                'intercom': True,
                'lights': True,
                'lights:groups': True,
                'lights:scenes': True,
                'lights:lights': True,
                'lights:schedules': True,
                'messaging': True,
                'extras': True,
                'extras:games': True,
            }
        }
        return data

LOCAL_CONFIG = ShaLocalConfig()
