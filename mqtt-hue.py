from phue import Bridge
import paho.mqtt.client as mqtt
import logging
import time
import json

logging.basicConfig()

# REQUIRES PYTHON2
b = Bridge('10.0.1.111')
topic = "tester/huelights"

b.connect()
#print(b.get_api())

lights = b.lights

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	#print(msg.topic+" "+str(msg.payload[0]))
	data = json.loads(msg.payload)
	print(type(data))
	
	# messages follow format X:Y
	xy = data["colour"].split(":")
	print(xy)
	print(xy[0])
	print(xy[1])
	print("-------------------")
	
	lightnames = data["lightnames"].split(":")
	
	command = {
		'transitiontime': 30,
		'on': True,
		'bri': data["brightness"],
		# We don't need to create a new array and
		#	can just use[xy] but I am doing this for error checking sake
		'xy': [float(xy[0]), float(xy[1])]
	}
	
	b.set_light(lightnames, command)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.0.2.174", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
