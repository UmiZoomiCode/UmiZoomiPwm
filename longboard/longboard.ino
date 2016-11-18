#include <Servo.h>

Servo motor;

//States
int const ACCELERATING = 1;
int const CRUISING = 2;
int const SLOWING = 3;
int CurrentState = 2;

float Acceleration = 3;
float CurrentSpeed = 1500;
float TargetSpeed = CurrentSpeed;

float MaxSlowing = 75;
float MinimumSlowing = 1;
float CurrentDeceleration = 0;

/*
 * 1500 means stop
 * 2000 means full throttle forward
 * 1000 means full throlle reverse
 */

void Accelerate(float power)
{
  CurrentSpeed = 1500 + (500*power);
}

void Decellerate(float power)
{
  
}

void UpdateSpeed()
{
  motor.writeMicroseconds(CurrentSpeed);
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
      delay(10);
    }

    
    float power = (((cmdQ[1] * 10) + cmdQ[2]) / 100.0);
    
    float newSpeed;
    if(cmdQ[0] == 1)
    {
      //Serial.write("Go forward");
      newSpeed = 1500 + (500 * power);
      if(newSpeed > TargetSpeed)
      {
        CurrentState = ACCELERATING;
        TargetSpeed = newSpeed;
      }
      else 
      {
        CurrentState = SLOWING;
        CurrentDeceleration = MinimumSlowing;
        TargetSpeed = newSpeed;
      }
    }
    else if(cmdQ[0] == 0){
      //Serial.println("got a negative move");
      TargetSpeed = 1500;
      CurrentState = SLOWING;
      CurrentDeceleration = MaxSlowing * power;
      //Serial.println(String(CurrentDeceleration, DEC));
    }
  }
  
  switch(CurrentState)
  {
    case CRUISING:
    break;
    case ACCELERATING:
      //Will Change
      CurrentSpeed = TargetSpeed;
      UpdateSpeed();
      CurrentState = CRUISING;
    break;
    case SLOWING:
      if(CurrentSpeed == TargetSpeed)
      {
        CurrentState = CRUISING;
      }
      else
      {
        Serial.println(String(CurrentSpeed, DEC));
        CurrentSpeed -= CurrentDeceleration;
        if(CurrentSpeed < TargetSpeed)
          CurrentSpeed = TargetSpeed;
        Serial.println(String(CurrentSpeed, DEC));
      }
      UpdateSpeed();
    break;
  }
  delay(250);
}

