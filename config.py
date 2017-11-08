import sys
# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.widgets

#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

from kivy.uix.button import Button


class ConfigScreen(ScreenManager):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        splashScreen = Screen(name="configSplash")
        configSplash = ConfigSplash()
        configSplash.configBtn.bind(on_press=self.chgScreen)
        configSplash.parentalBtn.bind(on_press=self.chgScreen)
        splashScreen.add_widget(configSplash)

        parentalScreen = Screen(name="parental")
        parentalCtrls = ParentalControlsPanel()
        parentalScreen.add_widget(parentalCtrls)

    def chgScreen(self, instance):
        if instance.text == "Configuration":
            self.current = "config"
        elif instance.text == "Parental Controls":
            self.current = "parental"


class ConfigSplash(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ConfigSplash, self).__init__(**kwargs)
        self.cols = 1
        self.configBtn = Button(text="Configuration")
        self.parentalBtn = Button(text="Parental Controls")
        self.add_widget(self.configBtn)
        self.add_widget(self.parentalBtn)


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
        self.chgBtn = Button(text="Test")
        self.add_widget(self.chgBtn)
