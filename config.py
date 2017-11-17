"""
Structure
~~~~~~~~~
* ConfigScreenManager
  * ConfigSplash
    * ConfigScreen
    * ParentalControlsScreen

Keypad in C:\Python36\lib\site-packages\kivy\data
"""
import os
import subprocess
import sys

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.globals
import StetsonHomeAutomation.widgets

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget

#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FallOutTransition

#Widgets
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput


class ConfigScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ConfigScreenManager, self).__init__(**kwargs)

        #Screens
        splashScreen = Screen(name="configSplash")
        cfgAlarmsScreen = Screen(name="cfgAlarms")
        cfgPanesScreen = Screen(name="cfgPanes")
        cfgSystemScreen = Screen(name="cfgSystem")
        configScreen = Screen(name="configScreen")
        parentalScreen = Screen(name="parentalScreen")

        #Widgets
        configPanel = ConfigPanel()
        configSplash = ConfigSplash()
        cfgAlarmsPanel = CfgAlarmsPanel()
        cfgPanesPanel = CfgPanesPanel()
        cfgSystemPanel = CfgSystemPanel()
        parentalCtrls = ParentalControlsPanel()

        #Layouts
        configScreen.add_widget(configPanel)
        cfgAlarmsScreen.add_widget(cfgAlarmsPanel)
        cfgPanesScreen.add_widget(cfgPanesPanel)
        cfgSystemScreen.add_widget(cfgSystemPanel)
        parentalScreen.add_widget(parentalCtrls)
        splashScreen.add_widget(configSplash)
        self.add_widget(splashScreen)
        self.add_widget(configScreen)
        self.add_widget(cfgAlarmsScreen)
        self.add_widget(cfgPanesScreen)
        self.add_widget(cfgSystemScreen)
        self.add_widget(parentalScreen)

        #Connections
        configSplash.configBtn.bind(on_press=self.chgScreen)
        configSplash.parentalBtn.bind(on_press=self.chgScreen)

    def chgScreen(self, instance):
        if instance.text == "Configuration":
            self.current = "configScreen"
        elif instance.text == "Parental Controls":
            self.current = "parentalScreen"


class ConfigSplash(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ConfigSplash, self).__init__(**kwargs)
        self.cols = 1
        self.configBtn = Button(text="Configuration")
        self.parentalBtn = Button(text="Parental Controls")
        self.add_widget(self.configBtn)
        self.add_widget(self.parentalBtn)


class ConfigPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ConfigPanel, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 15

        self.labelTitle = Label(text="Configuration", size_hint=(.4, .2))
        self.btnAlarms = Button(text="Alarms", size_hint=(.4, .1))
        self.btnBack = Button(text="Back", size_hint=(.4, .1))
        self.btnIcons = Button(text="Icons", size_hint=(.4, .1))
        self.btnPanes = Button(text="Panes", size_hint=(.4, .1))
        self.btnScreenSaver = Button(text="Screen Saver", size_hint=(.4, .1))
        self.btnSystem = Button(text="System", size_hint=(.4, .1))

        self.add_widget(self.labelTitle)
        self.add_widget(self.btnAlarms)
        self.add_widget(self.btnIcons)
        self.add_widget(self.btnPanes)
        self.add_widget(self.btnScreenSaver)
        self.add_widget(self.btnSystem)
        self.add_widget(Label(size_hint=(.4, .1)))
        self.add_widget(self.btnBack)

        #Connections
        self.btnBack.bind(on_press=self.goBack)
        self.btnAlarms.bind(on_press=self.goConfig)
        self.btnIcons.bind(on_press=self.goConfig)
        self.btnPanes.bind(on_press=self.goConfig)
        self.btnScreenSaver.bind(on_press=self.goConfig)
        self.btnSystem.bind(on_press=self.goConfig)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configSplash"
        self.parent.manager.transition = RiseInTransition()

    def goConfig(self, instance):
        if instance.text == "Alarms":
            self.parent.manager.current = "cfgAlarms"
        if instance.text == "Panes":
            self.parent.manager.current = "cfgPanes"
        if instance.text == "System":
            self.parent.manager.current = "cfgSystem"


class CfgAlarmsPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(CfgAlarmsPanel, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 15

        self.labelTitle = Label(text="Configuration -- Alarms", size_hint=(.4, .2))
        _subLayout = GridLayout(cols=2)
        self.labelAudible = Label(text="Audible", size_hint=(.4, .2))
        self.labelLed = Label(text="LED", size_hint=(.4, .2))
        self.labelVisual = Label(text="Visual", size_hint=(.4, .2))
        self.swAudible = Switch(active=True)
        self.swLed = Switch(active=False)
        self.swVisual = Switch(active=True)
        self.btnBack = Button(text="Back", size_hint=(.4, .1))

        self.add_widget(self.labelTitle)
        _subLayout.add_widget(self.labelAudible)
        _subLayout.add_widget(self.swAudible)
        _subLayout.add_widget(self.labelLed)
        _subLayout.add_widget(self.swLed)
        _subLayout.add_widget(self.labelVisual)
        _subLayout.add_widget(self.swVisual)
        self.add_widget(_subLayout)
        self.add_widget(Label(size_hint=(.4, .1)))
        self.add_widget(self.btnBack)

        #Connections
        self.btnBack.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configScreen"
        self.parent.manager.transition = RiseInTransition()


class CfgPanesPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(CfgPanesPanel, self).__init__(**kwargs)
        self.cols = 1
        self.dirty = False
        self.spacing = 15
        global StetsonHomeAutomation.globals.LOCAL_CONFIG
        self.localConfig = StetsonHomeAutomation.globals.LOCAL_CONFIG

        self.labelTitle = Label(text="Configuration -- Panes", size_hint=(.4, .2))
        _subLayout = GridLayout(cols=2)
        self.labelAudio = Label(text="Audio", size_hint=(.4, .2))
        self.labelExtras = Label(text="Extras", size_hint=(.4, .2))
        self.labelGames = Label(text="     Games", size_hint=(.4, .2))
        self.labelIntercom = Label(text="     Intercom", size_hint=(.4, .2))
        self.labelLights = Label(text="Lights", size_hint=(.4, .2))
        self.labelMessaging = Label(text="Messaging", size_hint=(.4, .2))
        self.swAudio = Switch(active=True)
        self.swExtras = Switch(active=False)
        self.swGames = Switch(active=True)
        self.swIntercom = Switch(active=True)
        self.swLights = Switch(active=True)
        self.swMessaging = Switch(active=True)
        self.btnBack = Button(text="Back", size_hint=(.4, .1))

        self.add_widget(self.labelTitle)
        _subLayout.add_widget(self.labelAudio)
        _subLayout.add_widget(self.swAudio)
        _subLayout.add_widget(self.labelIntercom)
        _subLayout.add_widget(self.swIntercom)
        _subLayout.add_widget(self.labelLights)
        _subLayout.add_widget(self.swLights)
        _subLayout.add_widget(self.labelMessaging)
        _subLayout.add_widget(self.swMessaging)
        _subLayout.add_widget(self.labelExtras)
        _subLayout.add_widget(self.swExtras)
        _subLayout.add_widget(self.labelGames)
        _subLayout.add_widget(self.swGames)
        self.add_widget(_subLayout)
        self.add_widget(Label(size_hint=(.4, .1)))
        self.add_widget(self.btnBack)

        #Connections
        self.btnBack.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configScreen"
        self.parent.manager.transition = RiseInTransition()

    def registerChange(self, instance):
        self.dirty = True
        if 'Audio' in instance.text:
            self.localConfig.data['panes']['audio'] = self.swAudio.active()
            if self.swAudio.active():
                pass
        elif 'Lights' in instance.text:
            self.localConfig.data['panes']['lights'] = self.swAudio.active()
        elif 'Messaging' in instance.text:
            self.localConfig.data['panes']['messaging'] = self.swAudio.active()

class CfgSystemPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(CfgSystemPanel, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 15

        self.labelTitle = Label(text="Configuration -- System", size_hint=(.4, .2))
        _subLayout = GridLayout(cols=2)
        self.labelHost = Label(text="Host Name", size_hint=(.4, .2))
        hostname = os.environ['COMPUTERNAME']
        self.valueHost = Label(text=hostname, size_hint=(.4, .2))
        self.labelIp = Label(text="IP Address", size_hint=(.4, .2))
        output = subprocess.run('ipconfig', check=True, stdout=subprocess.PIPE)
        ipAddr = "Unknown"
        for line in output.stdout.split(b"\n"):
            if b'IPv4' in line:
                ipAddr = str(line).split(":")[1].strip().replace("\\r'", "")
        self.valueIp = Label(text=ipAddr, size_hint=(.4, .2))
        self.btnBack = Button(text="Back", size_hint=(.4, .1))

        self.add_widget(self.labelTitle)
        _subLayout.add_widget(self.labelHost)
        _subLayout.add_widget(self.valueHost)
        _subLayout.add_widget(self.labelIp)
        _subLayout.add_widget(self.valueIp)
        self.add_widget(_subLayout)
        self.add_widget(Label(size_hint=(.4, .1)))
        self.add_widget(self.btnBack)

        #Connections
        self.btnBack.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configScreen"
        self.parent.manager.transition = RiseInTransition()


class LoginScreen(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="Password:"))
        self.password = TextInput(multiline=False)
        self.add_widget(self.password)

        #https://kivy.org/docs/api-kivy.core.window.html
        #https://kivy.org/docs/api-kivy.uix.vkeyboard.html
        self.add_widget(NumericKeyboard())

        self.backBtn = Button(text="Back")
        self.add_widget(self.backBtn)

        #Connections
        self.backBtn.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configSplash"
        self.parent.manager.transition = RiseInTransition()


class ParentalControlsPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ParentalControlsPanel, self).__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 50

        self.lockToggle = Button(text="Lock", size_hint=(.25, .25))
        self.controlsBtn = Button(text="Parental Controls", size_hint=(.25, .25))

        self.add_widget(self.lockToggle)
        self.add_widget(self.controlsBtn)
        self.backBtn = Button(text="Back")
        self.add_widget(self.backBtn)

        #Connections
        self.backBtn.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configSplash"
        self.parent.manager.transition = RiseInTransition()






class NumericKeyboard(Widget):
    #https://github.com/kivy/kivy/blob/master/examples/keyboard/main.py
    def __init__(self, **kwargs):
        kbMode = Config.get("kivy", "keyboard_mode")
        if not kbMode == 'systemandmulti':
            Config.set("kivy", "keyboard_mode", 'systemandmulti')
            Config.write()
            kbMode = Config.get("kivy", "keyboard_mode")
        print("Keyboard Mode: {}".format(kbMode))
        super(NumericKeyboard, self).__init__(**kwargs)
        kb = Window.request_keyboard(
            self._keyboard_close, self)
        if kb.widget:
            self._keyboard = kb.widget
            self._keyboard.layout = 'numeric.json'
        else:
            self._keyboard = kb
        self._keyboard.bind(on_key_down=self.key_down, on_key_up=self.key_up)

    def _keyboard_close(self):
        print('My keyboard has been closed!')
        self._keyboard.unbind(on_key_down=self.key_down)
        self._keyboard.unbind(on_key_up=self.key_up)
        self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def key_up(self, keyboard, keycode, *args):
        if isinstance(keycode, tuple):
            keycode = keycode[1]
        print("Key up {}".format(keycode))

