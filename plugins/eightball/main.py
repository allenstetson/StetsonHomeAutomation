import random

# Kivy imports
import kivy
kivy.require ('1.10.0')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.title = "Fortune Teller"

        self.add_widget(Label(text="Ask a yes/no question.."))
        self.askBtn = Button(text="Seek my wisdom")
        self.add_widget(self.askBtn)
        self.answerLabel = Label(text="")
        self.add_widget(self.answerLabel)

        self.askBtn.bind(on_press=self._pickAnswer)

    def _pickAnswer(self, instance):
        answers = [
            "Yes.",
            "No.",
            "Answer is unclear, ask later.",
            "Of course!",
            "Not for some time, but yes.",
            "It does not appear so.",
            "Definitely not!"
        ]
        ans = random.choice(answers)
        self.answerLabel.text = ans

        buttonText = [
            "Determine your fortune.",
            "Devise the answer.",
            "Tap into the mystic energies.",
            "Seek my wisdom."
        ]
        self.askBtn.text = random.choice(buttonText)