#include "rf.h"
#include "motor.h"
#include "sensors.h"
#include <LoRa.h>

unsigned long lastCommandTime = 0;
static bool failsafeActive = false;

void initRF() {
  LoRa.begin(915E6);
  lastCommandTime = millis();
}

void readCommand() {

  int packetSize = LoRa.parsePacket();

  if (packetSize) {

    String cmd = LoRa.readString();

    int f, t, v;

    // expected format: F:1500,T:1500,V:1500
    if (sscanf(cmd.c_str(), "F:%d,T:%d,V:%d", &f, &t, &v) == 3) {

      // pwm values between 1000 and 2000
      f = constrain(f, 1000, 2000);
      t = constrain(t, 1000, 2000);
      v = constrain(v, 1000, 2000);

      updateMotors(f, t, v);

      lastCommandTime = millis();
    }
  }

  // stop motors if no command received for 1 second
  if (millis() - lastCommandTime > 1000) {
    if (!failsafeActive){
    updateMotors(1500, 1500, 1500);
    }
  }
}

void sendTelemetry() {

  updateIMU();

  float batt = readBattery();
  float depth = readDepth();

  LoRa.beginPacket();

  // battery %
  LoRa.print("B:");
  LoRa.print(batt);

  // depth (meters)
  LoRa.print(",D:");
  LoRa.print(depth);

  // acceleration
  LoRa.print(",AX:");
  LoRa.print(ax);
  LoRa.print(",AY:");
  LoRa.print(ay);
  LoRa.print(",AZ:");
  LoRa.print(az);

  // pitch (degrees)
  LoRa.print(",P:");
  LoRa.print(pitch);
  // roll (degrees)
  LoRa.print(",R:");
  LoRa.print(roll);
}