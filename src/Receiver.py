#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import string
import random
from utils import MockClient

def create_std_receiver(topic: str):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(10))

    return ReceiverMqtt(receiver_id=id, topic=topic)

def on_message_wrapper(proper_closure: callable):
    def on_message_refactor(client, userdata, message):
        entry_message = (str(message.payload.decode("utf-8")))
        proper_closure(entry_message)
    return on_message_refactor

class ReceiverMqtt:
    def __init__(self, receiver_id: str, topic: str, broker_name: str="localhost"):
        self.client = mqtt.Client()
        self.broker_address = broker_name
        self.id = receiver_id
        self.topic = topic

    def subscribe_and_start_observing(self, on_proper_closure: callable):
        self.client.on_message = on_message_wrapper(on_proper_closure)
        self.client.loop_start()
        self.client.subscribe(self.topic)

    def connect_to_broker(self):
        self.client.connect(self.broker_address)

    def disconnect_from_broker(self):
        self.client.disconnect()

if __name__ == "__main__":
    env=create_std_receiver('top')
