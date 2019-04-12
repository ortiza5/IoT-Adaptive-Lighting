from flask import Flask, render_template, flash, redirect
from flask_mqtt import Mqtt
import ssl
import subprocess
import atexit
import time
from config import *

# verify with 'netstat -at'
subprocess.Popen('sudo mosquitto -c /etc/mosquitto/mosquitto.conf', shell=True)
time.sleep(5)
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '0.0.0.0'
app.config['MQTT_BROKER_PORT'] = 8883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
# TLS Settings
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_INSECURE'] = True
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2
app.config['MQTT_TLS_CA_CERTS'] = '/etc/mosquitto/ca_certificates/ca.crt'
mqtt = Mqtt(app)
app.secret_key = SECRET


# Startpage
@app.route('/')
def startpage():
    return render_template('startpage.html')


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

def exit_handler():
    # subprocess.Popen('sudo mosquitto -c /etc/mosquitto/mosquitto.conf', shell=True)
    print('My application is ending!')


if __name__ == '__main__':
    atexit.register(exit_handler)
    # sudo mosquitto -c /etc/mosquitto/mosquitto.conf
    # subprocess.Popen('sudo mosquitto -c /etc/mosquitto/mosquitto.conf', shell=True)
    app.run(host="0.0.0.0", debug=True)
