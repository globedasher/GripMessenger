# comms.py to run the communcations of grip.py

#Module imports
import paho.mqtt.client as mqtt


class Connection():
    """ This is the connection class. The MQTT client is created here.
    """
    def __init__(self):
        # Instantiate the client at tag client.
        client = mqtt.Client(
                client_id=str(random.random()),
                clean_session=True,
                userdata=user_name
                )

        # The following lines define the on_connect and on_message callbacks
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        #self.client.on_publish = self.on_publish

        # Use loop_start() before connecting to recieve the on_connect
        # callback.
        self.client.loop_start()
        self.client.connect("iot.eclipse.org", 1883, 60)

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

    def on_message(self, client, userdata, msg):
        """Callback triggered when a message is recieved.
        """
        #print(userdata)
        #print(msg.topic)
        #print(msg.payload)
        # Decode the msg.payload from bytearray to UTF-8 then cat onto the
        # message_display.
        payload = pickle.loads(msg.payload)
        print(payload)
        self.message_display.text += "%s %s %s: %s\n" % (
                payload["date"],
                payload["time"],
                payload["name"],
                payload["text"]
                )

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            client.publish(
                    "grip/pub/connect",
                    "Disconnected",
                    qos=0,
                    retain=True,
                    )
            print("Unexpected disconnect")
        else:
            print("Disconnect Complete")
