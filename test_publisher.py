import paho.mqtt.client as paho
import time
import json

# Had issues connecting to broker on Duckietown network
# broker = 'broker1'
# port = 8883

# Public development broker (TEMP)
broker = 'broker.hivemq.com'
port = 1883

connected_flag = False

def on_connect(client, userdata, flags, rc):
	global conn_flag
	connected_flag = True
	print('Connected', connected_flag)

def on_log(client, userdata, level, buf):
	print('Buffer ', buf)

def on_disconnect(client, userdata, rc):
	print('Client Lighting disconnected')

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


# Create the MQTT Client for the LED Light Control
client_lighting = paho.Client('client_server1222211')
client_lighting.on_log = on_log
# Development broker is not using TLS
# client_lighting.tls_set('/home/pi/ca.crt',tls_version=2)
client_lighting.on_connect = on_connect
client_lighting.on_disconnect = on_disconnect
client_lighting.on_publish = on_publish

# Connect to the broker
client_lighting.connect(broker, port)
client_lighting.loop_start() #start the loop

# while not connected_flag:
# 	time.sleep(1)
# 	client_lighting.loop()
payload1 = json.dumps([1,2,3,4,5,6,7,45])
payload2 = json.dumps(dict(
	red=1,
	green=147,
	blue=41,
	brightness=0.7,
	number=60,
	mode="Localized"
))

# client_lighting.publish('lights/strip1', payload1, 1)
client_lighting.publish('configurations/strip1', payload2, 1)

time.sleep(1) # wait
client_lighting.loop_stop() #stop the loop

