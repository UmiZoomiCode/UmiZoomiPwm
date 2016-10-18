
#Accelerator Thread Test

import AcceleratorThread as at
from threading import Thread

s = {"maxSpeed" : 0, "currentSpeed" : 0, "acceleration" : 2, "deceleration": 10}

thread = Thread(target=at.Accelerate, args=(s,))
thread.start()

while(True):
	newSpeed = int(input("Input new speed 0 - 99"))
	s['maxSpeed'] = newSpeed