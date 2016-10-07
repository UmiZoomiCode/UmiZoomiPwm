import pwmcontroller as pw
import time

pwm = pw.changeSpeed(1.0)

time.sleep(2)

pwm.stop()

pwm = pw.stop()

time.sleep(2)

pwm.stop()