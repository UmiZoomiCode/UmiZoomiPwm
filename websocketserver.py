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
            print(self.data)
            msg = json.loads(self.data)

            if(msg['msg'] == "ChangeSpeed"):
                newSpeed = int(msg["speed"])
                
                if(newSpeed >= 100):
                    newSpeed = 99
                
                s["maxSpeed"] = newSpeed
                print(s["maxSpeed"])

        except Exception as e:
            print(str(e))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

    


if __name__ == "__main__":
    server = SimpleWebSocketServer('', 8000, PWMConverter)
    server.serveforever()