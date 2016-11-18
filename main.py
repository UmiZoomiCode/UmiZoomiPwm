import bluetoothConnector as bt
#import websocketserver as wss
import ArduinoInterface as at

from threading import Thread
from time import sleep

s = {"maxSpeed" : 0, "currentSpeed" : 0, "acceleration" : 2, "deceleration": 10}
newSpeed = 0

if __name__ == "__main__":
    # server = SimpleWebSocketServer('', 8000, PWMConverter)
    # server.serveforever()

    #accelerator = Thread(target=at.Accelerate, args=(s,))
    #accelerator.start()

    controller = bt.PS3_Controller()
    currentSpeed = 0
    while True:
        controller.check_status()
        #print(controller.buttons)
        if controller.buttons != None:
            newSpeed = int(float(controller.buttons['r3']) * 100) * -1
            # print("newSpeed: " + str(newSpeed))
            # print("currentSpeed: " + str(currentSpeed))
            # if the speed difference +- 15
            if(int(controller.buttons['r1']) == 0):
                if(newSpeed - currentSpeed >= 5 or currentSpeed - newSpeed >= 5):
                    #print("changing")
                    # print(controller.buttons)
                    # if(int(controller.buttons['r3']) <= -1):
                    #     controller.buttons['r3'] = .99
                    print("changing speed: " + str(newSpeed))
                    currentSpeed = newSpeed
                    at.ChangeSpeed(currentSpeed)

            # if(int(controller.buttons['r1']) == 0):
                # controller.sendMessage("{\"msg\": \"ChangeSpeed\",\"speed\" : "+str(newSpeed * -1)+"}")
        sleep(0.5) 
