# =============================================================================
# Imports
#  =============================================================================
# stdlib
import json
import requests
import sys

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.lights
import StetsonHomeAutomation.audio
import StetsonHomeAutomation.config

# Kivy imports
import kivy
kivy.require ('1.10.0')

from kivy.app import App

#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

#Misc
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior

#Widgets
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


# =============================================================================
# Globals
# =============================================================================
STATUS_BAR = Label(text="Problem detected.", size_hint=(1, .1))
ACTIVE_AUDIO_IN = []
ACTIVE_AUDIO_OUT = []
WEBROOT = "http://localhost:8082/"


# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================
class ImageButton(ButtonBehavior, Image):
    pass

class GridLayoutWithBg(GridLayout):
    def __init__(self, **kwargs):
        super(GridLayoutWithBg, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class AccordionWithBg(Accordion):
    def __init__(self, **kwargs):
        super(AccordionWithBg, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size



class MessagingPanel(GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(MessagingPanel, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Messaging is currently disabled."))


class CarouselInterface(Carousel):
    def __init__(self, **kwargs):
        super(CarouselInterface, self).__init__(**kwargs)
        self.statusBar = STATUS_BAR
        self.add_widget(StetsonHomeAutomation.config.ConfigScreen(transition=RiseInTransition()))
        self.audioPanel = StetsonHomeAutomation.audio.AudioPanel(self)
        self.add_widget(self.audioPanel)
        self.lightPanel = StetsonHomeAutomation.lights.LightPanel(self)
        self.add_widget(self.lightPanel)
        self.add_widget(MessagingPanel())
        self.index = 1

    def on_index(self, inst, pos):
        super(CarouselInterface, self).on_index(inst, pos)
        if self.index == 0:
            self.statusBar.text = "Stetson House - (Unlocked)"
        elif self.index == 1:
            currIn = self.audioPanel.activeAudioIn or "None"
            currOut = ", ".join(self.audioPanel.activeAudioOutBtns) or "None"
            self.statusBar.text = "Stetson House - ({} : {})".format(currIn, currOut)
        elif self.index == 2:
            self.lightPanel.tracker.UpdateLightsStatus() #Allen tight coupling - delegate
        else:
            self.statusBar.text = "Stetson House"

class MainDisplay(GridLayout):
    def __init__(self):
        super(MainDisplay, self).__init__()
        STATUS_BAR.text="Stetson House - (XM Radio : Kitchen, Family Room, Back Yard)"
        self.cols = 1
        self.add_widget(STATUS_BAR)
        self.add_widget(CarouselInterface())


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(MainDisplay(self))


class ParentalSettingsScreen(Screen):
    def __init__(self, name=None, **kwargs):
        super(ParentalSettingsScreen, self).__init__(**kwargs)
        self.add_widget(Label(text="Settings go here"))


class MessagingPanelLo(GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(MessagingPanelLo, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Messaging is currently disabled."))


class MyBetterApp(App):
    def build(self):
        self.title="StetsonHomeAutomation"
        return MainDisplay()


# =============================================================================
if __name__ == "__main__":
    app = MyBetterApp()
    app.run()
