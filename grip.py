# This is the grip.py file for the matching grip.kv file

import os, sys, _thread


from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from datetime import datetime

import paho.mqtt.client as mqtt

#import comms

print("Welcome to Grip Messenger!")

# NOTE: I am creating a temporily hard coded user name to send and receive
# messages.
user_name = "rocko"
message_stack = []

# TODO: Enter button send function.
# TODO: Display text in non-editable form.
# TODO: If user_name is blank, present dialog to request name.
# TODO: Cat new messages onto message stack.



def on_connect(client, userdata, flags, rc):
    print ("Connected with result code " +str(rc))
    # Subscribing in on_connect() means:
    # If we lose the connection and reconnect, subscriptions will be renewed.
    #print(flags)
    #print(userdata)
    #client.publish("grip/pub/connect", "Client connect", qos=0, retain=True)
    client.subscribe("grip/messages", qos=0)
    print("Connected")

def on_disconnect(client, userdata, flags):
    client.publish("grip/pub/connect", "Disconnected", qos=0, retain=True)

def on_message(client, userdata, msg):
    print("on_message")
    print(msg.topic + " " + str(msg.payload))


class HomeScreen(Screen):
    """ The HomeScreen widget is the first view loaded of the UI.
    """
    message_input = ObjectProperty(None)
    message_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Creates all the initial conditions for the HomeScreen.
        """
        # TODO: What does this *super* call do exactly?
        super(HomeScreen, self).__init__(**kwargs)
        # The following lines define the on_connect and on_message callbacks


    def send(self, data):
        """Send uses the publish() method to send data to the MQTT broker.
        """
        #print(data.text)
        # TODO: change payload to be dictionary with more attributes for each
        # message.
        payload = str(datetime.now()) + " " + user_name + ": " + data.text
        #message_stack.append(payload)
        #print(message_stack)
        #print(self.message_display.text)
        #print(self.message_input.text)
        self.client.publish("grip/messages", payload, qos=0)
        # DONE: Refresh the text display.
        self.message_display.text += payload + "\n"
        data.text = ""

    def on_enter(self, data):
        """This function allows an enter to send a message.
        """
        self.send(data)

    def disconnect(self):
        print("used method")
        self.client.disconnect()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_start()


# DONE: This class creates the Main Application!
class GripApp(App):
    def build(self):
        return HomeScreen()


# The following lines instantiate and run the application.
if __name__ == "__main__":
    GripApp().run()
