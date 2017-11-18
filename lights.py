# =============================================================================
# Imports
#  =============================================================================
# stdlib imports
import sys
import colorsys
import requests

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.globals
import StetsonHomeAutomation.widgets

# Kivy imports
import kivy
kivy.require ('1.10.0')

#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem

#Widgets
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker

# =============================================================================
# Globals
# =============================================================================

# =============================================================================
# Functions
# =============================================================================


# =============================================================================
# Classes
# =============================================================================
class LightColorPicker(BoxLayout):
    def __init__(self, **kwargs):
        super(LightColorPicker, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.picker = ColorPicker()
        self.applyBtn = Button(text="Apply Changes", size_hint=(1, .1))
        self.closeBtn = Button(text="Close", size_hint=(1, .1))
        self.add_widget(self.picker)
        self.add_widget(self.applyBtn)
        self.add_widget(self.closeBtn)

class LightStateTracker(object):
    def __init__(self, caller=None):
        self.caller = caller
        self.lights = []
        self.activeLights = []
        self.allGroups = {}
        self.scenes = []
        self.webroot = StetsonHomeAutomation.globals.WEBROOT
        self.LoadInitialLightStates()

    def LoadInitialLightStates(self):
        # Lights/Groups
        try:
            response = requests.get(self.webroot+"get/lifx/lights/all")
            if response.status_code == requests.codes.ok:
                self.lights = response.json()
            else:
                raise NetworkError("Cannot get light data: {}".format(response.status_code))
            for light in self.lights:
                if light['connected'] and light['power'] == "on":
                    self.activeLights.append(light['label'])
                if not light['group']['name'] in self.allGroups:
                    self.allGroups[light['group']['name']] = {}
                    self.allGroups[light['group']['name']]['lights'] = []
                    self.allGroups[light['group']['name']]['id'] = light['group']['id']
                self.allGroups[light['group']['name']]['lights'].append(light['label'])
        except requests.exceptions.ConnectionError:
            self.caller.statusBar.text = "Error connecting to internet - check modem health!"
            for light in self.lights:
                light.color = [.1, .1, .1, 1]

        # Scenes
        try:
            self.scenes = requests.get(self.webroot+"get/lifx/scenes").json()
        except requests.exceptions.ConnectionError:
            self.caller.statusBar.text = "Error connecting to server.!"

    def UpdateLightsStatus(self):
        if not self.activeLights:
            msg = "None"
        else:
            msg = ", ".join(self.activeLights)
        self.caller.statusBar.text = "Stetson House - (%s)" % msg

    def add(self, item):
        if not item in self.activeLights:
            self.activeLights.append(item)

    def remove(self, item):
        if item in self.activeLights:
            self.activeLights.remove(item)

class LightPanel(StetsonHomeAutomation.widgets.AccordionWithBg):
    def __init__(self, caller, **kwargs):
        super(LightPanel, self).__init__(**kwargs)
        self.tracker = LightStateTracker(caller)
        self.caller = caller
        self.statusBar = caller.statusBar
        self.webroot = StetsonHomeAutomation.globals.WEBROOT

        self.orientation = "vertical"

        ## GROUPS
        self.groups = AccordionItem(title="Groups")
        #self.groups.add_widget(Button(text="All Groups", background_color=[0, .35, .7, 1]))
        # Whole House
        _btn_layout = BoxLayout(orientation='vertical')
        btn = StetsonHomeAutomation.widgets.ImageButton()
        btn.text = "Stetson House"
        btn.id = 'stetsonHouse'
        btn.source = "resource/icons/lifxIconGroup.png"
        btn.bind(on_press=self.handleGroupPressed)
        _btn_layout.add_widget(btn)
        _btn_layout.add_widget(Label(text=btn.text))
        self.groups.add_widget(_btn_layout)

        for groupName in self.tracker.allGroups:
            text = groupName+"\n"
            text += "{} lights\n".format(len(self.tracker.allGroups[groupName]['lights']))
            lightsOn = []
            lightsOff = []
            for light in self.tracker.allGroups[groupName]['lights']:
                if light in self.tracker.activeLights:
                    lightsOn.append(light)
                else:
                    lightsOff.append(light)
            text += "({} On, {} Off)".format(len(lightsOn), len(lightsOff))
            _btn_layout = BoxLayout(orientation='vertical')
            btn = StetsonHomeAutomation.widgets.ImageButton()
            btn.text = text
            btn.id = self.tracker.allGroups[groupName]['id']
            btn.source = "resource/icons/lifxIconLight.png"
            btn.bind(on_press=self.handleLightPressed)
            _btn_layout.add_widget(btn)
            _btn_layout.add_widget(Label(text=btn.text))
            self.groups.add_widget(_btn_layout)
            #self.groups.add_widget(Button(text=text, background_color=[0,.35,.7,1]))
        self.add_widget(self.groups)

        ## SCENES
        item = AccordionItem(title="Scenes")
        for scene in self.tracker.scenes:
            text = scene['name']+"\n"
            text += "{} lights".format(len(scene['states']))
            _btn_layout = BoxLayout(orientation='vertical')
            btn = StetsonHomeAutomation.widgets.ImageButton()
            btn.text = text
            btn.id = scene['uuid']
            btn.source = "resource/icons/lifxIconLight.png"
            btn.bind(on_press=self.handleScenePressed)
            _btn_layout.add_widget(btn)
            _btn_layout.add_widget(Label(text=btn.text))
            item.add_widget(_btn_layout)
        self.add_widget(item)

        ## LIGHTS
        self.accordianLights = AccordionItem(title="Lights")
        self.allLightButtons = list()

        # Whole House
        _btn_layout = BoxLayout(orientation='vertical')
        btn = StetsonHomeAutomation.widgets.ImageButton()
        btn.text = "Stetson House"
        btn.id = 'stetsonHouse'
        btn.source = "resource/icons/lifxIconGroup.png"
        btn.bind(on_press=self.handleGroupPressed)
        _btn_layout.add_widget(btn)
        _btn_layout.add_widget(Label(text=btn.text))
        self.accordianLights.add_widget(_btn_layout)

        # Individual Lights
        for light in self.tracker.lights:
            _btn_layout = BoxLayout(orientation='vertical')
            btn = StetsonHomeAutomation.widgets.ImageButton()
            btn.text = light['label']
            btn.id = light['id']
            btn.source = "resource/icons/lifxIconLight.png"
            btn.bind(on_press=self.handleLightPressed)
            self.setLightButtonColor(btn, data=self.tracker.lights)
            self.allLightButtons.append(btn)
            _btn_layout.add_widget(btn)
            _btn_layout.add_widget(Label(text=btn.text))
            self.accordianLights.add_widget(_btn_layout)

        self.add_widget(self.accordianLights)

        item = AccordionItem(title="Schedules")
        item.add_widget(LightColorPicker())
        #item.add_widget(Button(text="Off1222a", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="LvgRoomOn", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="PirateOn", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="Vaca On 19:37", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="PirateOff", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="BedroomOn", background_color=[0,.35,.7,1]))
        #item.add_widget(Button(text="LvgRoomOff", background_color=[0,.35,.7,1]))
        self.add_widget(item)
        self.page = 1
        self.groups.collapse = False

    def handleLightPressed(self, instance):
        #Query State
        try:
            url = self.webroot+"get/lifx/lights/id/{}".format(instance.id)
            responseQuery = requests.get(url)
            responseQueryData = responseQuery.json()
            light = responseQueryData[0]
            if not light['connected']:
                instance.color = [.1, .1, .1, 1]
                self.statusBar.text = 'Error: light "{}" is not connected.'.format(instance.text)
                return
            if light['power'] == 'on':
                newPower = 'off'
                self.setLightButtonColor(instance, power=newPower, data=responseQueryData)
                self.tracker.remove(instance.text)
            else:
                newPower = 'on'
                self.setLightButtonColor(instance, power=newPower, data=responseQueryData)
                self.tracker.add(instance.text)
            self.statusBar.text = "Turning light \"%s\" %s" % (instance.text, newPower)

            #Set State
            data = {
                'power': newPower,
             }
            url = self.webroot+'set/lifx/lights/id:{}/state'.format(instance.id)
            response = requests.put(url, params=data)
        except requests.exceptions.ConnectionError:
            self.statusBar.text = "Error connecting to server."

    def handleGroupPressed(self, instance):
        #Query State
        urlQuery = self.webroot+'get/lifx/location'
        try:
            responseQuery = requests.get(urlQuery)
            responseQueryData = responseQuery.json()
        except requests.exceptions.ConnectionError:
            self.statusBar.text = 'Error connecting to server.'
            return

        anythingOn = False
        for light in responseQueryData:
            if light['connected']:
                if light['power'] == 'on':
                    anythingOn = True
                    break
        if anythingOn:
            newPower = 'off'
            instance.color = [.3, .3, .3, 1]
            for button in self.allLightButtons:
                self.setLightButtonColor(button, power=newPower, data=responseQueryData)
            for light in responseQueryData:
                self.tracker.remove(light)
        else:
            newPower = 'on'
            instance.color = [1, 1, 1, 1]
            for button in self.allLightButtons:
                self.setLightButtonColor(button, power=newPower, data=responseQueryData)
            for light in responseQueryData:
                self.tracker.add(light)
        self.statusBar.text = "Turning \"%s\" %s" % (instance.text, newPower)

        #Set State
        data = {
            'power': newPower,
         }
        try:
            url = self.webroot+'set/lifx/location/state'
            response = requests.put(url, data=data)
        except requests.exceptions.ConnectionError:
            self.statusBar.text = 'Error connecting to server.'

    def handleScenePressed(self, instance):
        pass

    def setLightButtonColor(self, button, power=None, data=None):
        if not data:
            raise NotImplementedError("Don't be lazy, send me the response query. I'm not done yet.")
        light = None
        for lgt in data:
            if lgt['id'] == button.id:
                light = lgt
                break
        if not light:
            return #Likely a light in a different location
        if not power:
            power = light['power']
        if not light['connected']:
            button.color = [.1, .1, .1, 1]
        elif power == 'off':
            button.color = [.3, .3, .3, 1]
        elif power == 'on':
            if 'hue' in light['color'] and 'saturation' in light['color']:
                hue = light['color']['hue'] * 0.0027777777
                brightness = light['brightness'] / 2.0
                currColor = colorsys.hls_to_rgb(hue,
                                                brightness,
                                                light['color']['saturation'],
                                                )
                brightPercent = int(light['brightness'] * 100)
                button.text = "{} ({}%)".format(light['label'], brightPercent)
                button.color = [currColor[0], currColor[1], currColor[2], 1]
            else:
                button.color = [1, 1, 1, 1]
        else:
            raise ValueError("Unsupported value for power: %s" % power)

#------------------------------------------------------------------------------

class NetworkError(RuntimeError):
    def __init__(self, args):
        self.args = args