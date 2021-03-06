# comms.py to run the communcations of grip.py

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code " +str(rc))
    # Subscribing in on_connect() means:
    # If we lose the connection and reconnect, subscriptions will be renewed.
    #print(flags)
    #print(userdata)
    #client.publish("grip/pub/connect", "Client connect", qos=0, retain=True)
    client.subscribe("grip/pub/connect", qos=0)
    client.subscribe("grip/messages", qos=0)
    print("Connected!")

def on_disconnect(client, userdata, flags, rc):
    if rc != 0:
        print("Unexpected disconnect")


def on_message(client, userdata, msg):
    print("on_message")
    print(str(msg.payload))
    #print(msg.topic + " " + str(msg.payload))

print("comms on here?")
client = mqtt.Client()

# The following lines define the on_connect and on_message callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
