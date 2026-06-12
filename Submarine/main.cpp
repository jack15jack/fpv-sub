#include "motor.h"
#include "rf.h"
#include "sensors.h"

unsigned long lastTelemetry = 0;

void setup() {
  initMotors();
  initRF();
  initSensors();
}

void loop() {

  readCommand(); // receive control commands

  if (millis() - lastTelemetry > 300) {
    sendTelemetry();
    lastTelemetry = millis();
  }
}