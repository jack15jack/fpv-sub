#include "sensors.h"
#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <Sparkfun_MS5837.h>

#define BATTERY_PIN A0
#define BATTERY_SCALE 4.2

Adafruit_LIS3DH imu = Adafruit_LIS3DH();
MS5837 depth;

static float ax = 0;
static float ay = 0;
static float az = 0;

static float pitch = 0;
static float roll = 0;

void initSensors(){
  pinMode(BATTERY_PIN, INPUT);

  Wire.begin();

  // Initialize IMU
  if (!imu.begin(0x18)){
    Serial.println("Could not start IMU");
    while(1);
  }

  imu.setRange(LIS3DH_RANGE_2_G);
  imu.setDataRate(LIS3DH_DATARATE_50_HZ);

  // Initialize depth sensor
  if (!depth.init()){
    Serial.println("Could not start depth sensor");
    while(1);
  }

  depth.setFluidDensity(997); // fresh water
}

float readBattery(){

  int raw = analogRead(BATTERY_PIN);

  float voltage = raw * (5.0 / 4095.0) * BATTERY_SCALE;

  return voltage;
}

void updateIMU(){
  sensors_event_t event;
  imu.getEvent(&event);

  ax = event.acceleration.x;
  ay = event.acceleration.y;
  az = event.acceleration.z;

  pitch = atan2(-ax, sqrt(ay*ay+az*az)) * 180.0 / PI;
  roll = atan2(ay, az) * 180.0 / PI;
}

float getAccelX(){ return ax; }
float getAccelY(){ return ay; }
float getAccelZ(){ return az; }
float getPitch(){ return pitch; }
float getRoll(){ return roll; }

float readDepth(){
  depth.read();
  return depth.depth();
}