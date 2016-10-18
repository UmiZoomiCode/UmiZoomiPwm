#include <Servo.h>

Servo motor;

/*
 * 1500 means stop
 * 2000 means full throttle forward
 * 1000 means full throlle reverse
 */

void stop(){
  motor.writeMicroseconds(1500);
}

void driveForward(float percent)
{
  if(percent > 1.0){
    percent = 1.0;
  }
  else if(percent < 0.0){
    percent = 0.0;
  }
  motor.writeMicroseconds(1500 + (500*percent));
}

void driveReverse(float percent){
  if(percent > 1.0){
    percent = 1.0;
  }
  else if(percent < 0.0){
    percent = 0.0;
  }
  
  stop();
  delay(150);
  motor.writeMicroseconds(1300);
  delay(150);
  stop();
  delay(150);
  motor.writeMicroseconds(1500 - (500 * percent));
}

void setup()
{
  motor.attach(6); // attaches motor to pin d6
  
  motor.writeMicroseconds(1500);
  Serial.begin(9600);
}

void loop()
{
  Serial.flush();
  int cmdQ[3];
  int byte = 0;
  
  if(Serial.available()){

    // example message 150 = 1, forward at 50% power
    
    for(int n = 0; n < 3; n++){
      if(Serial.available()) cmdQ[n] = Serial.read() - '0';
      Serial.println(cmdQ[n]);
      delay(10);
    }
    
    
    float power = (((cmdQ[1] * 10) + cmdQ[2]) / 100.0);

    if(cmdQ[0] == 1)
    {
      driveForward(power);
    }
    else if(cmdQ[0] == 0){
      Serial.println("stopping");
      stop();
    }
    
  }
  
  delay(250);
}

