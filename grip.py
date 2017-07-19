# This is the grip.py file for the matching grip.kv file

import os, sys


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget

import comms

print("Welcome to Grip Messenger!")

# NOTE: I am creating a temporily hard coded user name to send and receive
# messages.
user_name = "rocko"

class HomeScreen(Screen):
    """ The HomeScreen widget is the first view loaded of the UI.
    """
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode[1])
        if keycode[1] == 'enter':
            self.send(self.text_input)
        return True

    def send(self, data):
        """Send uses the publish() method to send data to the MQTT broker.
        """
        print(data.text)
        comms.client.publish(user_name + "/messages", data.text, qos=0)
        data.text = ''


# DONE: This class creates the Main Application!
class GripApp(App):
    def build(self):
        return HomeScreen()


# The following lines instantiate and run the application.
if __name__ == "__main__":
    GripApp().run()
