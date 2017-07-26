# This is the grip.py file for the matching grip.kv file

#Module imports
import os, sys, _thread, pickle, random, datetime
import paho.mqtt.client as mqtt

from .comms import Connection


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


print("Welcome to Grip Messenger!")

# NOTE: I am creating a temporily hard coded user name to send and receive
# messages.
user_name = "vilan"
message_stack = []

# TODO: Display text in non-editable form.
# TODO: If user_name is blank, present dialog to request name.


class HomeScreen(Screen, Connection):
    """ The HomeScreen widget is the first view loaded of the UI.
    """
    message_input = ObjectProperty(None)
    message_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Creates all the initial conditions for the HomeScreen.
        """
        # TODO: What does this *super* call do exactly?
        super(HomeScreen, self).__init__(**kwargs)

    def on_enter(self, data):
        """This function allows an enter to send a message.
        """
        self.send(data)

    def send(self, data):
        """Send uses the publish() method to send data to the MQTT broker.
        """
        # data is the object passed from the kivy app TextInput function
        # data.text is the actual text from that object.
        # TODO: change payload to be dictionary with more attributes for each
        # message.
        payload = {
                "name": user_name,
                "text": data.text,
                "date": str(datetime.date.today()),
                "time": str(datetime.time()),
                }
        ppayload = pickle.dumps(payload)
        self.client.publish("grip/messages", ppayload, qos=0)
        # TODO: Track success of publish with return_value.
        data.text = ""

    def on_publish(self, client, userdata, mid):
        #print(mid)
        pass

    def disconnect(self):
        """Disconnect from the MQTT server and stop the application.
        """
        self.client.disconnect()
        print("Performed disconnect")
        app.stop()



# DONE: This class creates the Main Application!
class GripApp(App):
    def build(self):
        return HomeScreen()


# The following lines instantiate and run the application.
if __name__ == "__main__":
    app = GripApp()
    #print(app)
    app.run()
