from flask import Flask, render_template, flash, redirect
from flask_mqtt import Mqtt
import ssl
import subprocess
import atexit
import time
from config import *

# Activate python enviroment:
# source env/bin/activate

# Deactivate python enviroment:
# deactivate
# =========================================================================
# Global Variables:
intensity = 1
r_val = 255
b_val = 255
g_val = 255
num_leds = 300
length = 5	#(in meters)
leds_per_m = num_leds/length

# =========================================================================
# Start the MQTT broker in another thread:
# Service stopped in the exithandler function (CTRL-C)
# verify with 'netstat -at'
subprocess.Popen('sudo mosquitto -c mosquitto.conf', shell=True)
# Sleep to allow password to be entered (TODO - find a better way)
time.sleep(5)

# =========================================================================
# Start the Flask App and Configure MQTT 
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '0.0.0.0'
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 0.5  # refresh time in seconds
# TLS Settings
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_INSECURE'] = True
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2
app.config['MQTT_TLS_CA_CERTS'] = '/etc/mosquitto/ca_certificates/ca.crt'
mqtt = Mqtt(app)
app.secret_key = SECRET

# =========================================================================
# ****************************HTML Pages***********************************
# =========================================================================
# Startpage
@app.route('/')
def startpage():
	return render_template('startpage.html')

@app.route('/activity_log')
def activity_log():
	return render_template('activity_log.html')

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
	print(data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
	print(level, buf)

# =========================================================================
# ***************************Helper Functions******************************
# =========================================================================
# Called when CTRL-C is pressed to cleanly stop the MQTT broker
def exit_handler():
	print('Stopping Mosquitto')
	subprocess.Popen('sudo service mosquitto stop', shell=True)
	print('The application is closing')

# =========================================================================
# Start up the app
if __name__ == '__main__':
	atexit.register(exit_handler)
	app.run(host="0.0.0.0", debug=True)
