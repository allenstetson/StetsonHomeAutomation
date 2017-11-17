# =============================================================================
# Imports
#  =============================================================================
import kivy
kivy.require ('1.10.0')

# Kivy Imports
#Layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.accordion import Accordion, AccordionItem

#Misc
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior

#Widgets
from kivy.uix.image import Image

# =============================================================================
# Globals
# =============================================================================

# =============================================================================
# Functions
# =============================================================================


# =============================================================================
# Classes
# =============================================================================
class ImageButton(ButtonBehavior, Image):
    pass


class ColoredBoxLayout(BoxLayout):
    def __init__(self, color, **kwargs):
        super(ColoredBoxLayout, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source="resource/icons/bgGrad.png", pos=self.pos, size=self.size)
            #Color(color)
        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


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


