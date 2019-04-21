import paho.mqtt.client as paho
import time

# Had issues connecting to broker on Duckietown network
# broker = 'broker1'
# port = 8883

# Public development broker (TEMP - TODO: Get local version working)
broker = 'broker.hivemq.com'
port = 1883

connected_flag = False

def on_connect(client, userdata, flags, rc):
	global connected_flag
	connected_flag = True
	print('Connected', connected_flag)

def on_log(client, userdata, level, buf):
	print('Buffer ', buf)

def on_disconnect(client, userdata, rc):
	print('Client disconnected')

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")





def localization_func():
	# TODO: Add localization reading
	return ''




# Create the MQTT Client for the LED Light Control
client_loc = paho.Client('localization-client001')

# Development broker is not using TLS (TODO: Re-add if local version is working)
# client_loc.tls_set('/home/pi/ca.crt',tls_version=2)

client_loc.on_connect = on_connect
client_loc.on_log = on_log
client_loc.on_disconnect = on_disconnect
client_loc.on_publish = on_publish

# Connect to the broker
client_loc.connect(broker, port)
client_loc.loop_start() #start the loop

while True:
	results = localization_func()
	client_loc.publish('lights/strip1', results, 1)

client_loc.loop_stop() #stop the loop

