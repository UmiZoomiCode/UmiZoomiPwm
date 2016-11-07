#!/usr/bin/python
import serial
import struct
import json

import AcceleratorThread as at

from threading import Thread
from time import sleep
from pprint import pprint
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

s = {"maxSpeed" : 0, "currentSpeed" : 0, "acceleration" : 2, "deceleration": 10}

accelerator = Thread(target=at.Accelerate, args=(s,))
accelerator.start()

class PWMConverter(WebSocket):

    def handleMessage(self):
        global s
        try:
            msg = json.loads(self.data)
            # pprint(msg)
            if(msg['msg'] == "ChangeSpeed"):
                newSpeed = int(msg["speed"])
                print(newSpeed)
                
                if(newSpeed >= 100):
                    print("TOO MUCH")
                    newSpeed = 99
                
                s["maxSpeed"] = newSpeed

        except Exception as e:
            print("error: " + str(e))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

    


if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8000, PWMConverter)
    server.serveforever()