#include "motor.h"
#include <Servo.h>

// ESC objects
static Servo forward;
static Servo turn;
static Servo vertical;

#define ESC_FORWARD_PIN 3
#define ESC_TURN_PIN 5
#define ESC_VERTICAL_PIN 6

/*
PWM range:
 1000 us -> full reverse
 1500 us -> neutral
 2000 us -> full forward
*/

void initMotors() {

  forward.attach(ESC_FORWARD_PIN);
  turn.attach(ESC_TURN_PIN);
  vertical.attach(ESC_VERTICAL_PIN);

  forward.writeMicroseconds(1500);
  turn.writeMicroseconds(1500);
  vertical.writeMicroseconds(1500);

  delay(2000);
}

void updateMotors(int f, int t, int v) {

  forward.writeMicroseconds(f);
  turn.writeMicroseconds(t);
  vertical.writeMicroseconds(v);
}