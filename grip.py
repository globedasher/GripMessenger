# This is the grip.py file for the matching grip.kv file

#Module imports
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

#Local imports
#import comms

print("Welcome to Grip Messenger!")

# NOTE: I am creating a temporily hard coded user name to send and receive
# messages.
user_name = "Rocko"
message_stack = []

# TODO: Display text in non-editable form.
# TODO: If user_name is blank, present dialog to request name.


class HomeScreen(Screen):
    """ The HomeScreen widget is the first view loaded of the UI.
    """
    message_input = ObjectProperty(None)
    message_display = ObjectProperty(None)

    def __init__(self, client, **kwargs):
        """ Creates all the initial conditions for the HomeScreen.
        """
        # TODO: What does this *super* call do exactly?
        super(HomeScreen, self).__init__(**kwargs)

        # The following lines define the on_connect and on_message callbacks
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        #self.client.on_publish = self.on_publish
        self.client.connect("iot.eclipse.org", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """This callback is triggered when the MQTT client connects to the
        server.
        """
        print("Connected with result code " +str(rc))
        #print("Let's roll!")
        # Subscribing in on_connect() means:
        # If we lose the connection and reconnect, subscriptions will be renewed.
        #print("User name: %s" % userdata)
        client.publish(
                "grip/pub/connect",
                "%s has connected" % userdata,
                qos=0,
                retain=True
                )

        client.subscribe("grip/messages", qos=0)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            client.publish("grip/pub/connect", "Disconnected", qos=0, retain=True)
            print("Unexpected disconnect")
        else:
            print("Disconnect Complete")

    #def on_publish(self, client, userdata, mid):
        #print(mid)

    # DONE: Cat new messages onto view
    def on_message(self, client, userdata, msg):
        """Callback triggered when a message is recieved.
        """
        #print(userdata)
        #print(msg.topic)
        #print(msg.payload)
        # Decode the msg.payload from bytearray to UTF-8 then cat onto the
        # message_display.
        self.message_display.text += (
                "%s said: %s \n" % (
                    userdata,
                    str(msg.payload.decode('utf-8'))))

    def send(self, data):
        """Send uses the publish() method to send data to the MQTT broker.
        """
        #data is the object passed from the kivy app TextInput function

        #print(data.text)
        # TODO: change payload to be dictionary with more attributes for each
        # message.
        payload = data.text
        #message_stack.append(payload)
        #print(message_stack)
        #print(self.message_display.text)
        #print(self.message_input.text)
        return_value = self.client.publish("grip/messages", payload, qos=0)
        #print(return_value)
        if return_value[0] != 0:
            print("Send error")
        else:
            print("Sent")
            #print("Messge id: %d" % return_value[1])
        # DONE: Refresh the text display.
        #self.message_display.text += payload + "\n"
        data.text = ""

    # DONE: Enter button send function.
    def on_enter(self, data):
        """This function allows an enter to send a message.
        """
        self.send(data)

    def disconnect(self):
        """Disconnect from the MQTT server and stop the application.
        """
        self.client.disconnect()
        print("Performed disconnect")
        app.stop()


# DONE: This class creates the Main Application!
class GripApp(App):
    def build(self):
        # Instantiate the client at tag client.
        client = mqtt.Client(
                client_id="12999",
                clean_session=True,
                userdata=user_name
                )

        return HomeScreen(client)


# The following lines instantiate and run the application.
if __name__ == "__main__":
    app = GripApp()
    print(app)
    app.run()
