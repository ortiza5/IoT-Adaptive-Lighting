from flask import Flask, render_template, flash, redirect
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import ssl
import subprocess
import atexit
import time
import json
from config import *

# Activate python enviroment:
# source venv/bin/activate

# Deactivate python enviroment:
# deactivate
# =========================================================================
# Global Variables:
x_loc = 0
y_loc = 0
intensity = 1
r_val = 255
b_val = 255
g_val = 255
num_leds = 300
length = 5	#(in meters)
leds_per_m = num_leds/length

# Using Development Broker
# # =========================================================================
# # Start the MQTT broker in another thread:
# # Service stopped in the exithandler function (CTRL-C)
# # verify with 'netstat -at'
# subprocess.Popen('sudo mosquitto -c mosquitto.conf', shell=True)
# # Sleep to allow password to be entered (TODO - find a better way)
# time.sleep(5)
# subprocess.Popen('python3 on-server-client.py')
# =========================================================================
# Start the Flask App and Configure MQTT 
app = Flask(__name__)
# Development Broker Used Instead
# app.config['MQTT_BROKER_URL'] = '0.0.0.0'
# app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.1  # refresh time in seconds
# TLS Settings
app.config['MQTT_TLS_ENABLED'] = False
# Using Development Broker Instead without TLS
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2
# app.config['MQTT_TLS_CA_CERTS'] = '/etc/mosquitto/ca_certificates/ca.crt'
mqtt = Mqtt(app)
socketio = SocketIO(app)
app.secret_key = SECRET

# =========================================================================
# ****************************HTML Pages***********************************
# =========================================================================
# Startpage
@app.route('/')
def startpage():
	return render_template('startpage.html')

@app.route('/console_log')
def console_log():
	return render_template('console_log.html')

@app.route('/mapping')
def mapping():
	return render_template('mapping.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
	return render_template('settings.html')

# =========================================================================
# **************************MQTT Functions*********************************
# =========================================================================
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	data = dict(
		topic=message.topic,
		payload=message.payload.decode()
	)
	print('\nGot A message\n')
	socketio.emit('mqtt_rec', data=data)
	processing(data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
	print(level, buf)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	mqtt.subscribe('lights/strip1')

@mqtt.on_publish()
def handle_publish(client,userdata,result):
	data = dict(
		x=x_loc,
		y=y_loc
	)
	print('data published')
	socketio.emit('mqtt_pub', data=data)


# =========================================================================
# ***************************Helper Functions******************************
# =========================================================================
# Called when CTRL-C is pressed to cleanly stop the MQTT broker
def exit_handler():
	# print('\nStopping Mosquitto')
	# subprocess.Popen('service mosquitto stop', shell=True)
	print('The application is closing')

def processing(data):
	global x_loc
	global y_loc

	print('Hello')
	x_loc = int(data['payload'])+10
	new_data = json.dumps(dict(		# encodes the dictionary as a json to send
		x=x_loc,
		y=y_loc
	))
	mqtt.publish('locations/strip1', new_data)

# =========================================================================
# Start up the app
if __name__ == '__main__':
	atexit.register(exit_handler)
	socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True)
