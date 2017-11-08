import kivy
kivy.require ('1.10.0')

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.pagelayout import PageLayout
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


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


class ParentalControlsPanel(GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(ParentalControlsPanel, self).__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 50
        #self.screenManager = MyScreenManager()

        self.lockToggle = Button(text="Lock", size_hint=(.25, .25))
        self.controlsBtn = Button(text="Parental Controls", size_hint=(.25, .25))
        self.controlsBtn.bind(on_press=self.switchScreens)

        self.add_widget(self.lockToggle)
        self.add_widget(self.controlsBtn)

    def switchScreens(self, state):
        #self.screenManager.current ='settings'
        pass


class MessagingPanel(GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(MessagingPanel, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Messaging is currently disabled."))


class LoginScreen(GridLayoutWithBg):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Username:"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="Password:"))
        self.password = TextInput(multiline=False)
        self.add_widget(self.password)


class AudioPanel(AccordionWithBg):
    def __init__(self, **kwargs):
        super(AudioPanel, self).__init__(**kwargs)

        self.orientation = "vertical"
        item = AccordionItem(title="Presets")
        item.add_widget(Label(text="No presets defined."))
        item.collapse = True
        self.add_widget(item)

        self.inputs = AccordionItem(title="Inputs")
        self.inputs.add_widget(Button(text="Entertainment System", background_color=[0,.35,.7,1]))
        self.inputs.add_widget(Button(text="XM Radio", background_color=[0,.35,.7,1]))
        self.inputs.add_widget(Button(text="PC (Carterpie)", background_color=[0,.35,.7,1]))
        self.inputs.add_widget(Button(text="Laptop (Jolteon)", background_color=[0,.35,.7,1]))
        self.inputs.add_widget(Button(text="CD Player", background_color=[0,.35,.7,1]))
        self.add_widget(self.inputs)

        item = AccordionItem(title="Outputs")
        item.add_widget(Button(text="Back Yard", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Kitchen", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Dining", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Family Room", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Master Bedroom", background_color=[0,.35,.7,1]))
        item.collapse = True
        self.add_widget(item)

        item = AccordionItem(title="Intercom")
        item.add_widget(Button(text="Push to Talk", background_color=[0,.35,.7,1]))
        item.collapse = True
        self.add_widget(item)
        self.inputs.collapse = False


class LightPanel(AccordionWithBg):
    def __init__(self, **kwargs):
        super(LightPanel, self).__init__(**kwargs)

        self.orientation = "vertical"

        self.groups = AccordionItem(title="Groups")
        self.groups.add_widget(Button(text="All Groups", background_color=[0,.35,.7,1]))
        self.groups.add_widget(Button(text="Bedroom", background_color=[0,.35,.7,1]))
        self.groups.add_widget(Button(text="Dining", background_color=[0,.35,.7,1]))
        self.groups.add_widget(Button(text="Living Room", background_color=[0,.35,.7,1]))
        self.add_widget(self.groups)

        item = AccordionItem(title="Scenes")
        item.add_widget(Button(text="Movie Night", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Party Lights", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Pool Party", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="TV Room", background_color=[0,.35,.7,1]))
        self.add_widget(item)

        item = AccordionItem(title="Lights")
        item.add_widget(Button(text="My Home", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Allen", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Ji Sun", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="LIFX TV Room 1", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="LIFX TV Room 2", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Pirate Lamp", background_color=[0,.35,.7,1]))
        self.add_widget(item)

        item = AccordionItem(title="Schedules")
        item.add_widget(Button(text="Off1222a", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="LvgRoomOn", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="PirateOn", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="Vaca On 19:37", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="PirateOff", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="BedroomOn", background_color=[0,.35,.7,1]))
        item.add_widget(Button(text="LvgRoomOff", background_color=[0,.35,.7,1]))
        self.add_widget(item)
        self.page = 1
        self.groups.collapse = False


class CarouselInterface(Carousel):
    def __init__(self, **kwargs):
        super(CarouselInterface, self).__init__(**kwargs)
        self.add_widget(ParentalControlsPanel())
        self.add_widget(AudioPanel())
        self.add_widget(LightPanel())
        self.add_widget(MessagingPanel())
        self.index = 1

    def on_index(self, inst, pos):
        super(CarouselInterface, self).on_index(inst, pos)
        self.statusBar = Label()
        if self.index == 0:
            root.statusBar.text = "Stetson House - (Unlocked)"
        elif self.index == 1:
            root.statusBar.text = "Stetson House - (XM Radio : Kitchen, Family Room, Back Yard)"
        elif self.index == 2:
                root.statusBar.text = "Stetson House - (Bedroom, Pirate Lamp)"
        else:
            root.statusBar.text = "Stetson House"


class MainDisplay(GridLayout):
    def __init__(self):
        super(MainDisplay, self).__init__()
        self.statusBar = Label(
            text="Stetson House - (XM Radio : Kitchen, Family Room, Back Yard)", size_hint=(1, .1))
        self.cols = 1
        self.add_widget(self.statusBar)
        self.add_widget(CarouselInterface())


class OnlyOne:
    class __OnlyOne:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne(arg)
        else:
            OnlyOne.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)




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
        return MainDisplay()


if __name__ == "__main__":
    app = MyBetterApp()
    app.run()
