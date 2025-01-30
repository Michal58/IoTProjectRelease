#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
from config import * 

from namespace import MQTT_ID_AND_MESSAGE_SEPARATOR
from utils import MockClient

from datetime import datetime
import random
import string

def create_std_sender(topic: str):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(10))

    return SenderMqtt(sender_id=id, topic=topic)

class SenderMqtt:
    def __init__(self, sender_id: str, topic: str, broker_name: str="localhost"):
        self.client = mqtt.Client()
        self.broker_address = broker_name
        self.id = sender_id
        self.channel = topic
        
    def publishMessage(self, message: str):
        self.client.publish(self.channel, message)

    def connect_to_broker(self):
        self.client.connect(self.broker_address)

    def disconnect_from_broker(self):
        self.client.disconnect()


if __name__ == "__main__":
    env=SenderMqtt()
    print(env)
