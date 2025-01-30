from ast import main
from typing import List, Tuple
import json

class MockClient:
    def __init__(self):
        pass
    def publish(self, channel, message):
        pass
    def connect(self,broker_address):
        pass
    def loop_start(self):
        pass
    def subscribe(self,topic):
        pass

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    in_rank=[
            ['abc',100],
            ['efg',200],
            ['hij',300]
        ]
    print('in rank')
    print(in_rank)
