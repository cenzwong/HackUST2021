

import json
from importlib import import_module

class thingsboard_MQTT:
    """
    Thingsboard MQTT Client
    -----------------------
    # pip install paho-mqtt
    """
    ############## Pub ####################
    

    def __init__(self, SERVER ,ACCESS_TOKEN, PORT = 1883, MQTT_ALIVE = 60):
        """
        SERVER ,
        ACCESS_TOKEN, 
        PORT = 1883, 
        MQTT_ALIVE = 60
        -----------Notes-----------------
        The default port is 1883
        e.g: thingsboard_MQTT(SERVER="demo.thingsboard.io", ACCESS_TOKEN="abcdefg")
        """
        mqtt = import_module('paho.mqtt.client')
        
        self.MQTT_SERVER = SERVER
        self.MQTT_PORT = PORT
        self.MQTT_ALIVE = MQTT_ALIVE
        self.MQTT_TOPIC1 = "v1/devices/me/telemetry"
        self.ACCESS_TOKEN = ACCESS_TOKEN
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.username_pw_set(self.ACCESS_TOKEN)
        self.mqtt_client.connect(self.MQTT_SERVER, self.MQTT_PORT, self.MQTT_ALIVE)
        self.mqtt_client.loop_start()

    def push(self, payload):
        """
        payload is the python dictionary
        -----------Notes-----------------
        payload = {}
        payload["time"] = time.asctime( time.localtime(time.time()) )
        payload["test"] = 10010
        tb.push(payload)
        """
        self.mqtt_client.publish(topic=self.MQTT_TOPIC1, payload=json.dumps(payload), qos=2)
        
class thingsboard_HTTPs:
    """
    Thingsboard HTTPs Client
    -----------------------
    """
    def __init__(self, SERVER ,ACCESS_TOKEN, PORT = 443, HTTPs = "https"):
        """
        tb = thingsboard_HTTPs(SERVER="demo.thingsboard.io", ACCESS_TOKEN="abcdefg")
        tb2 = thingsboard_HTTPs(SERVER="demo.thingsboard.io", ACCESS_TOKEN="zh2idXN4qqNyVO1MNkGW", HTTPs = "http", PORT = 80)
        """
        self.requests = import_module('requests')
        
        self.HTTPs_SERVER = SERVER
        self.HTTPs_PORT = PORT
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.HTTPs = HTTPs
        
        url_base = '{HTTPs}://{SERVER}:{PORT}/api/v1/{ACCESS_TOKEN}/telemetry'
        self.HTTPs_URL = url_base.format(
                                            HTTPs = self.HTTPs, 
                                            SERVER = self.HTTPs_SERVER,
                                            PORT = self.HTTPs_PORT,
                                            ACCESS_TOKEN = self.ACCESS_TOKEN            
                                           )
        
        
    def push(self, payload):
        """
        payload = {}
        payload["time"] = time.asctime( time.localtime(time.time()) )
        payload["test"] = 10010
        tb2.push(payload)
        """
        return self.requests.post(self.HTTPs_URL, json=payload)
    
