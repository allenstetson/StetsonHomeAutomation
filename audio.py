"""
Structure
~~~~~~~~~
v AudioPanel
  v PresetsPanel
  v OutputsPanel
    > OutputsContainer
      v OutputsBox| v ControlsBox
        > Row1HBox   * btns
          * btns
        > Row2HBox
          * btns
  v InputsPanel
    > InputsContainer
      v InputsBox| v ControlsBox
        > Row1HBox   * btns
          * btns
        > Row2HBox
          * btns
  v Intercom Panel
  
"""

# =============================================================================
# Imports
#  =============================================================================
# stdlib
import json
import requests
import sys

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.widgets

# Kivy imports
import kivy
kivy.require ('1.10.0')

#Layouts
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout

#Widgets
from kivy.uix.label import Label
from kivy.uix.button import Button


# =============================================================================
# Globals
# =============================================================================
ACTIVE_AUDIO_IN = []
ACTIVE_AUDIO_OUT = []
WEBROOT = "http://localhost:8082/"


# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================
class AudioPanel(StetsonHomeAutomation.widgets.AccordionWithBg):
    def __init__(self, caller, **kwargs):
        super(AudioPanel, self).__init__(**kwargs)
        self.caller = caller
        self.statusBar = caller.statusBar
        self.allAudioSrcBtns = []
        self.allAudioOutBtns = []
        self.activeAudioOutBtns = []
        self.activeAudioIn = None

        self.orientation = "vertical"
        item = AccordionItem(title="Presets")
        item.add_widget(Label(text="No presets defined."))
        item.collapse = True
        self.add_widget(item)

        self.accordianInputs = AccordionItem(title="Inputs")
        self._makeInputsPanel()
        self.add_widget(self.accordianInputs)

        self.accordianOutputs = AccordionItem(title="Outputs")
        self._makeOutputsPanel()
        self.add_widget(self.accordianOutputs)

        item = AccordionItem(title="Intercom")
        item.add_widget(Button(text="Push to Talk", background_color=[0,.35,.7,1]))
        item.collapse = True
        self.add_widget(item)
        self.accordianInputs.collapse = False

        self._loadInitialStates()
        self._setupConnections()

    # -------------------------------------------------------------------------
    # Handlers
    # -------------------------------------------------------------------------
    def _handleAudioGenPressed(self, instance):
        instance.color = [1, 1, 1, 1]
        if instance.id == "power":
            if self.isAudioPowerOn:
                self.isAudioPowerOn = False
                instance.color = [.7, .7, .7, 1]
                turnOff = self.allAudioSrcBtns
                turnOff.extend([self.btnCntrlVolUp, self.btnCntrlVolDwn])
                for button in turnOff:
                    button.color = [.3, .3, .3, 1]
        try:
            response = requests.get(WEBROOT + "set/receiver/control/{0}".format(instance.id))
            responseData = json.loads(response.content)[0]
            self.statusBar.text = "Audio input set to {0}".format(instance.text)
        except requests.exceptions.ConnectionError:
            self.statusBar.text = \
                "Error encountered attempting to change receiver {0}".format(instance.text)

    def _handleAudioOutputPressed(self, instance):
        if instance.id in self.activeAudioOutBtns:
            instance.color = [.3, .3, .3, 1]
            self.activeAudioOutBtns.remove(instance.id)
        else:
            instance.color = [1, 1, 1, 1]
            self.activeAudioOutBtns.append(instance.id)

    def _handleAudioSourcePressed(self, instance):
        self.activeAudioIn = instance.text
        for button in self.allAudioSrcBtns:
            if button.text == instance.text:
                button.color = [1, 1, 1, 1]
            else:
                button.color = [.3, .3, .3, 1]
        try:
            response = requests.get(WEBROOT + "set/receiver/source/{0}".format(instance.id))
            responseData = json.loads(response.content)[0]
            self.statusBar.text = "Audio input set to {0}".format(instance.text)
        except requests.exceptions.ConnectionError:
            self.statusBar.text = \
                "Error encountered attempting to change input to {0}".format(instance.text)

    # -------------------------------------------------------------------------
    # Private Methods
    # -------------------------------------------------------------------------
    def _blinkButton(self, instance):
        instance.color = [.5, .5, .5, 1]

    def _inputButton(self, text, id, image):
        button = StetsonHomeAutomation.widgets.ImageButton()
        button.text = text
        button.id = id
        button.source = image
        button.bind(on_press=self._blinkButton)
        button.bind(on_release=self._handleAudioSourcePressed)
        _btn_layout = BoxLayout(orientation='vertical')
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(button)
        _btn_layout.add_widget(Label(text=text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .2)))
        return (button, _btn_layout)

    def _loadInitialStates(self):
        # FAKING Load Initial State
        self.isAudioPowerOn = self.getCurrentPowerState()
        if self.isAudioPowerOn:
            #self._togglePower("on")
            btn = self.getCurrentPowerState()
            #self._setCurrentIn(btn)
        else:
            self.btnCntrlPower.color = [.7, .7, .7, 1]
            #self._togglePower("off")
        for button in self.allAudioOutBtns:
            button.color = [.3, .3, .3, 1]

    def _makeControlsBox(self):
        controlsBox = StetsonHomeAutomation.widgets.ColoredBoxLayout(
            (1, 0, 0, 1),
            orientation='vertical',
            size_hint=(.2, 1)
        )

        _btn_layout = BoxLayout(orientation='vertical')
        self.btnCntrlPower = StetsonHomeAutomation.widgets.ImageButton()
        self.btnCntrlPower.text = "Power"
        self.btnCntrlPower.id = 'power'
        self.btnCntrlPower.source = "resource/icons/genIconPower.png"
        self.btnCntrlPower.bind(on_press=self._blinkButton)
        self.btnCntrlPower.bind(on_release=self._handleAudioGenPressed)
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(self.btnCntrlPower)
        _btn_layout.add_widget(Label(text=self.btnCntrlPower.text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .2)))
        controlsBox.add_widget(_btn_layout)

        _btn_layout = BoxLayout(orientation='vertical')
        self.btnCntrlMute = StetsonHomeAutomation.widgets.ImageButton()
        self.btnCntrlMute.text = "Mute"
        self.btnCntrlMute.id = 'mute'
        self.btnCntrlMute.source = "resource/icons/genIconMute.png"
        self.btnCntrlMute.bind(on_press=self._blinkButton)
        self.btnCntrlMute.bind(on_release=self._handleAudioGenPressed)
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(self.btnCntrlMute)
        _btn_layout.add_widget(Label(text=self.btnCntrlMute.text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .2)))
        controlsBox.add_widget(_btn_layout)

        _btn_layout = BoxLayout(orientation='vertical')
        self.btnCntrlVolUp = StetsonHomeAutomation.widgets.ImageButton()
        self.btnCntrlVolUp.text = "Volume Up"
        self.btnCntrlVolUp.id = 'volup'
        self.btnCntrlVolUp.source = "resource/icons/genIconUp.png"
        self.btnCntrlVolUp.bind(on_press=self._blinkButton)
        self.btnCntrlVolUp.bind(on_release=self._handleAudioGenPressed)
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(self.btnCntrlVolUp)
        _btn_layout.add_widget(Label(text=self.btnCntrlVolUp.text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .2)))
        controlsBox.add_widget(_btn_layout)

        _btn_layout = BoxLayout(orientation='vertical')
        self.btnCntrlVolDwn = StetsonHomeAutomation.widgets.ImageButton()
        self.btnCntrlVolDwn.text = "Volume Down"
        self.btnCntrlVolDwn.id = 'voldwn'
        self.btnCntrlVolDwn.source = "resource/icons/genIconDown.png"
        self.btnCntrlVolDwn.bind(on_press=self._blinkButton)
        self.btnCntrlVolDwn.bind(on_release=self._handleAudioGenPressed)
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(self.btnCntrlVolDwn)
        _btn_layout.add_widget(Label(text=self.btnCntrlVolDwn.text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .3)))
        controlsBox.add_widget(_btn_layout)

        return controlsBox

    def _makeInputsPanel(self):
        inputsContainer = BoxLayout(orientation="horizontal")
        inputsBox = BoxLayout(orientation="vertical")
        _btnRow1 = BoxLayout(orientation='horizontal')
        
        #AM/FM
        (self.btnAudioSrcAmFm, _btn_layout) = self._inputButton(
            "AM/FM Radio",
            "amfm",
            "resource/icons/audioIconAmFm.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcAmFm)

        #XM
        (self.btnAudioSrcXm, _btn_layout) = self._inputButton(
            "XM Radio",
            "xm",
            "resource/icons/audioIconXm.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcXm)

        #CD
        (self.btnAudioSrcCd, _btn_layout) = self._inputButton(
            "CD Player",
            "cd",
            "resource/icons/audioIconCd.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcCd)

        #Alexa
        (self.btnAudioSrcAlexa, _btn_layout) = self._inputButton(
            "Alexa",
            "alexa",
            "resource/icons/audioIconAlexa.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcAlexa)

        inputsBox.add_widget(_btnRow1)
        _btnRow2 = BoxLayout(orientation='horizontal')

        # EntSys
        (self.btnAudioSrcEntSys, _btn_layout) = self._inputButton(
            "Entertainment System",
            "entsys",
            "resource/icons/audioIconEntSys.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcEntSys)

        # PC
        (self.btnAudioSrcPc, _btn_layout) = self._inputButton(
            "PC (Caterpie)",
            "pc",
            "resource/icons/audioIconPc.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcPc)

        # Laptop
        (self.btnAudioSrcLaptop, _btn_layout) = self._inputButton(
            "Laptop (Joleton)",
            "laptop",
            "resource/icons/audioIconLaptop.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcLaptop)

        # Turntable
        (self.btnAudioSrcTurntable, _btn_layout) = self._inputButton(
            "Turn Table",
            "turntable",
            "resource/icons/audioIconTurntable.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioSrcBtns.append(self.btnAudioSrcTurntable)

        inputsBox.add_widget(_btnRow2)
        inputsContainer.add_widget(inputsBox)
        controlsBox = self._makeControlsBox()
        inputsContainer.add_widget(controlsBox)
        self.accordianInputs.add_widget(inputsContainer)

    def _makeOutputsPanel(self):
        outputsContainer = BoxLayout(orientation="horizontal")
        outputsBox = BoxLayout(orientation="vertical")
        _btnRow1 = BoxLayout(orientation='horizontal')

        # Master Bed
        (self.btnAudioOutMBed, _btn_layout) = self._outputButton(
            "Master Bedroom",
            "mbed",
            "resource/icons/audioIconOutMasterBed.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutMBed)

        # Master Bath
        (self.btnAudioOutMBath, _btn_layout) = self._outputButton(
            "Master Bathroom",
            "mbath",
            "resource/icons/audioIconOutMasterBath.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutMBath)

        # Asher Bed
        (self.btnAudioOutBed1, _btn_layout) = self._outputButton(
            "Asher's Bedroom",
            "bed1",
            "resource/icons/audioIconOutBed.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutBed1)

        # Owen Bed
        (self.btnAudioOutBed2, _btn_layout) = self._outputButton(
            "Owen's Bedroom",
            "bed2",
            "resource/icons/audioIconOutBed.png"
        )
        _btnRow1.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutBed2)

        outputsBox.add_widget(_btnRow1)
        _btnRow2 = BoxLayout(orientation='horizontal')

        # Jonah Bed
        (self.btnAudioOutBed3, _btn_layout) = self._outputButton(
            "Jonah's Bedroom",
            "bed3",
            "resource/icons/audioIconOutBed.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutBed3)

        # Upstairs Bath
        (self.btnAudioOutUpBath, _btn_layout) = self._outputButton(
            "Upstairs Bathroom",
            "upbath",
            "resource/icons/audioIconOutBath.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutUpBath)

        # Office
        (self.btnAudioOutOffice, _btn_layout) = self._outputButton(
            "Office",
            "office",
            "resource/icons/audioIconPc.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutOffice)

        # Living Room
        (self.btnAudioOutLiving, _btn_layout) = self._outputButton(
            "Living Room",
            "living",
            "resource/icons/audioIconOutSofa.png"
        )
        _btnRow2.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutLiving)

        outputsBox.add_widget(_btnRow2)
        _btnRow3 = BoxLayout(orientation='horizontal')

        # Kitchen
        (self.btnAudioOutKitchen, _btn_layout) = self._outputButton(
            "Kitchen",
            "kitchen",
            "resource/icons/audioIconOutKitchen.png"
        )
        _btnRow3.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutKitchen)

        # Family
        (self.btnAudioOutFamily, _btn_layout) = self._outputButton(
            "Family Room",
            "family",
            "resource/icons/audioIconOutTv.png"
        )
        _btnRow3.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutFamily)

        # Back Yard
        (self.btnAudioOutBkYard, _btn_layout) = self._outputButton(
            "Back Yard",
            "backyard",
            "resource/icons/audioIconOutPool.png"
        )
        _btnRow3.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutBkYard)

        # Garage
        (self.btnAudioOutGarage, _btn_layout) = self._outputButton(
            "Garage",
            "garage",
            "resource/icons/audioIconOutCar.png"
        )
        _btnRow3.add_widget(_btn_layout)
        self.allAudioOutBtns.append(self.btnAudioOutGarage)

        outputsBox.add_widget(_btnRow3)

        outputsContainer.add_widget(outputsBox)
        controlsBox = self._makeControlsBox()
        outputsContainer.add_widget(controlsBox)
        self.accordianOutputs.add_widget(outputsContainer)

    def _outputButton(self, text, id, image):
        button = StetsonHomeAutomation.widgets.ImageButton()
        button.text = text
        button.id = id
        button.source = image
        button.bind(on_press=self._blinkButton)
        button.bind(on_release=self._handleAudioOutputPressed)
        _btn_layout = BoxLayout(orientation='vertical')
        _btn_layout.add_widget(Label(text="", size_hint=(1, .1)))
        _btn_layout.add_widget(button)
        _btn_layout.add_widget(Label(text=text, size_hint=(1, .1)))
        _btn_layout.add_widget(Label(text="", size_hint=(1, .2)))
        return (button, _btn_layout)

    def _setupConnections(self):
        pass

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------
    def getCurrentAudioIn(self):
        try:
            response = requests.get(WEBROOT + "get/receiver/source/")
            responseData = json.loads(response.content)[0]
            for button in self.allAudioSrcBtns:
                if responseData['data'] == button.id:
                    button.color = [1, 1, 1, 1]
                else:
                    button.color = [.3, .3, .3, 1]
            return responseData['data']
        except requests.exceptions.ConnectionError:
            self.statusBar.text = \
                "Error encountered attempting to reach receiver"
            return "amfm" # ALLEN Faking data

    def getCurrentPowerState(self):
        try:
            response = requests.get(WEBROOT + "get/receiver/power/")
            responseData = json.loads(response.content)[0]
            if responseData['data'] == "on":
                self.isAudioPowerOn = True
            elif responseData['data'] == "off":
                self.isAudioPowerOn = False
            return self.isAudioPowerOn
        except requests.exceptions.ConnectionError:
            self.statusBar.text = \
                "Error encountered attempting to reach receiver"
            return False # ALLEN Faking data
