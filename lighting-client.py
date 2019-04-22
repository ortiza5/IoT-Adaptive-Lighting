import paho.mqtt.client as paho
import time
import neopixel
import board
import atexit
import json

LED_COUNT = 300
bf = 1.0 	# brightness factor
r_val = 255 # red value
b_val = 255	# blue value
g_val = 255 # green value
last_lit = [] # stores the last lit values

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
	message_out = str(msg.payload.decode("utf-8","ignore"))
	message_out = json.loads(message_out)
	if str(msg.topic) == "lights/strip1":
		# light up the indicated LEDS
		light_up(message_out)

	elif str(msg.topic) == "configurations/strip1":
		global r_val, g_val, b_val, bf, LED_COUNT
		# Set the new values from the message
		r_val = message_out['red']
		g_val = message_out['green']
		b_val = message_out['blue']
		bf = message_out['brightness']
		LED_COUNT = message_out['number']
		# refresh the lighting with new configuration
		light_up(last_lit)

def light_up(to_light):
	strip.fill((0, 0, 0))
	global last_lit
	last_lit = to_light

	for d in to_light:
		if d < LED_COUNT:
			strip[d] = (int(bf*r_val), int(bf*g_val), int(bf*b_val))
	strip.show()

# Called when CTRL-C is pressed
def exit_handler():
	for i in range(0,LED_COUNT):
		strip[i] = (0, 0, 0)
	strip.show()
	print('The application is closing')

# Create NeoPixel object with appropriate configuration.
LED_PIN = board.D18
# The order of the pixel colors - RGB or GRB
ORDER = neopixel.GRB
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=1.0, auto_write=False, pixel_order=ORDER)


atexit.register(exit_handler)

# Create the MQTT Client for the LED Light Control
client_lighting = paho.Client('client_lighting')
# Development broker is not using TLS
# client_lighting.tls_set('/home/pi/ca.crt',tls_version=2)
client_lighting.on_log = on_log
client_lighting.on_connect = on_connect
client_lighting.on_disconnect = on_disconnect
client_lighting.on_message = on_message

# Connect to the broker
client_lighting.connect(broker, port)

# Subscribe to the lights topic with sub topic strip1
client_lighting.subscribe('lights/strip1')
print('Subscribed to lights/strip1')
client_lighting.subscribe('configurations/strip1')
print('Subscribed to configurations/strip1')


client_lighting.loop_forever()

