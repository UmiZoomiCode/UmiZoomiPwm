try:
	import RPi.GPIO as gpio
except RuntimeError:
    print("rpi gpio was not imported. You probably need to use Sudo.")

gpio.setmode(GPIO.BOARD)
gpio.setup(40, GPIO.OUT)

maxSpeed = 9000

def changeSpeed(newValue):
 	return gpio.PWM(40, 9000 * newValue)

def stop():
	return gpio.PWM(40, 8000)
