# =============================================================================
# Imports
#  =============================================================================
# stdlib
import json
import os
import requests
import sys

# StetsonHomeAutomation imports
sys.path.insert(0, '..')
import StetsonHomeAutomation.audio
import StetsonHomeAutomation.config
import StetsonHomeAutomation.extras
import StetsonHomeAutomation.globals
import StetsonHomeAutomation.lights
import StetsonHomeAutomation.widgets

# Kivy imports
import kivy
kivy.require ('1.10.0')

from kivy.app import App

#Layouts
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import Screen, RiseInTransition

#Widgets
from kivy.uix.label import Label


# =============================================================================
# Globals
# =============================================================================

# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================
class MessagingPanel(StetsonHomeAutomation.widgets.GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(MessagingPanel, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Messaging is currently disabled."))


class CarouselInterface(Carousel):
    def __init__(self, **kwargs):
        super(CarouselInterface, self).__init__(**kwargs)
        self.localConfig = StetsonHomeAutomation.config.ShaLocalConfig()
        #global StetsonHomeAutomation.globals.STATUS_BAR
        self.statusBar = StetsonHomeAutomation.globals.STATUS_BAR

        #Widgets
        self.audioPanel = StetsonHomeAutomation.audio.AudioPanel(self)
        self.configPanel = StetsonHomeAutomation.config.ConfigScreenManager(
            transition=RiseInTransition())
        self.lightPanel = StetsonHomeAutomation.lights.LightPanel(self)
        self.extrasPanel = StetsonHomeAutomation.extras.ExtrasPanel(self)

        #Layouts
        self.add_widget(self.configPanel)
        self.updatePanes()
        self.index = 2
        self.configPanel.current = "configSplash"

    def updatePanes(self):
        if self.localConfig.data['panes']['audio']:
            try:
                self.add_widget(self.audioPanel)
            except kivy.uix.widget.WidgetException:
                #already added
                pass
        else:
            self.remove_widget(self.audioPanel)
        if self.localConfig.data['panes']['lights']:
            try:
                self.add_widget(self.lightPanel)
            except kivy.uix.widget.WidgetException:
                #already added
                pass
        else:
            self.remove_widget(self.lightPanel)
        if self.localConfig.data['panes']['messaging']:
            try:
                self.add_widget(MessagingPanel())
            except kivy.uix.widget.WidgetException:
                #already added
                pass
        else:
            self.remove_widget((MessagingPanel))
        self.add_widget(self.extrasPanel)


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
        #global StetsonHomeAutomation.globals.STATUS_BAR
        StetsonHomeAutomation.globals.STATUS_BAR.text="Stetson House - (XM Radio : Kitchen, Family Room, Back Yard)"
        self.cols = 1
        self.carousel = CarouselInterface()
        self.add_widget(StetsonHomeAutomation.globals.STATUS_BAR)
        self.add_widget(self.carousel)


class ParentalSettingsScreen(Screen):
    def __init__(self, name=None, **kwargs):
        super(ParentalSettingsScreen, self).__init__(**kwargs)
        self.add_widget(Label(text="Settings go here"))


class ShaApp(App):
    def build(self):
        self.title="StetsonHomeAutomation"
        return MainDisplay()


# =============================================================================
if __name__ == "__main__":
    #from kivy.core.window import Window
    #Window.fullscreen = True
    app = ShaApp()
    app.run()
