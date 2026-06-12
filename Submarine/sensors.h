#ifndef SENSORS_H
#define SENSORS_H

void initSensors();
float readBattery();
void updateIMU();
float getAccelX();
float getAccelY();
float getAccelZ();
float getPitch();
float getRoll();
float readDepth();

#endif