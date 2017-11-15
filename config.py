"""
Structure
~~~~~~~~~
* ConfigScreenManager
  * ConfigSplash
    * ConfigScreen
    * ParentalControlsScreen

Keypad in C:\Python36\lib\site-packages\kivy\data
"""
import sys
# StetsonHomeAutomation imports
sys.path.insert(0, '..')
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
from kivy.uix.textinput import TextInput


class ConfigScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(ConfigScreenManager, self).__init__(**kwargs)

        #Screens
        splashScreen = Screen(name="configSplash")
        configScreen = Screen(name="configScreen")
        parentalScreen = Screen(name="parentalScreen")

        #Widgets
        configPanel = LoginScreen()
        configSplash = ConfigSplash()
        parentalCtrls = ParentalControlsPanel()

        #Layouts
        configScreen.add_widget(configPanel)
        parentalScreen.add_widget(parentalCtrls)
        splashScreen.add_widget(configSplash)
        self.add_widget(splashScreen)
        self.add_widget(configScreen)
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


class ConfigPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ConfigPanel, self).__init__(**kwargs)
        self.cols = 1

        self.labelTitle = Label(text="Configuration")
        self.btnAlarms = Button(text="Alarms")
        self.btnBack = Button(text="Back")
        self.btnIcons = Button(text="Icons")
        self.btnPanes = Button(text="Panes")
        self.btnScreenSaver = Button(text="Screen Saver")
        self.btnSystem = Button(text="System")

        self.add_widget(self.labelTitle, size_hint=(1, .2))
        self.add_widget(self.btnAlarms, size_hint=(1, .1))
        self.add_widget(self.btnBack, size_hint=(1, .1))
        self.add_widget(self.btnIcons, size_hint=(1, .1))
        self.add_widget(self.btnPanes, size_hint=(1, .1))
        self.add_widget(self.btnScreenSaver, size_hint=(1, .1))
        self.add_widget(self.btnSystem, size_hint=(1, .1))

        #Connections
        self.backBtn.bind(on_press=self.goBack)

    def goBack(self, instance):
        self.parent.manager.transition = FallOutTransition()
        self.parent.manager.current = "configSplash"
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
