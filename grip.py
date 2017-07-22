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
from kivy.event import EventDispatcher
from datetime import datetime

import comms

print("Welcome to Grip Messenger!")

# NOTE: I am creating a temporily hard coded user name to send and receive
# messages.
user_name = "rocko"
message_stack = []

# TODO: Enter button send function.
# TODO: Display text in non-editable form.
# TODO: If user_name is blank, present dialog to request name.

class HomeScreen(Screen):
    """ The HomeScreen widget is the first view loaded of the UI.
    """
    message_input = ObjectProperty(None)
    message_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)


    def on_message_display(self, instance, value):
        print("The property changed to ", value)

    def send(self, data):
        """Send uses the publish() method to send data to the MQTT broker.
        """
        #print(data.text)
        # TODO: change payload to be dictionary with more attributes for each
        # message.
        payload = str(datetime.now()) + " " + user_name + ": " + data.text
        message_stack.append(payload)
        print(message_stack)
        comms.client.publish("grip/messages", payload, qos=0)
        print(self.message_display.text)
        print(self.message_input.text)
        # TODO: Cat new messages onto message stack.
        # DONE: Refresh the text display.
        self.message_display.text += self.message_input.text + "\n"
        data.text = ""


# DONE: This class creates the Main Application!
class GripApp(App):
    def build(self):
        return HomeScreen()


# The following lines instantiate and run the application.
if __name__ == "__main__":
    GripApp().run()
