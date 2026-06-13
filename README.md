# Autonomous FPV Submarine Drone

An open-source underwater remotely operated vehicle (ROV) designed for first-person-view (FPV) exploration, telemetry collection, and autonomous navigation experiments. The project combines embedded systems, robotics, wireless communication, and desktop software into a modular platform suitable for learning and experimentation.

---

## Overview

This project aims to develop a compact submarine capable of transmitting live video and telemetry to a surface base station while receiving real-time control commands from an operator.

Unlike traditional RC submarines, the vehicle is designed with a modular software architecture that separates hardware drivers, communication protocols, and control logic, making it easy to expand with additional sensors and autonomous behaviors.

The complete system consists of three major components:

* Submarine firmware
* Surface radio buoy
* Desktop base station

---

## Features

### Current

* Three independently controlled brushless thrusters
* LoRa command and telemetry communication
* Battery voltage monitoring
* Depth sensing
* IMU-based orientation sensing
* Motor failsafe if communication is lost
* Modular embedded firmware
* Python desktop control station
* Keyboard-based vehicle control

### Planned

* Analog FPV camera
* Surface radio buoy
* Live video streaming
* Xbox controller support
* Graphical desktop interface
* Data logging
* Leak detection
* Automatic depth hold
* Automatic heading hold
* Autonomous waypoint navigation
* Mission recording and playback

---

# System Architecture

```
+----------------------+
|   Desktop Computer   |
|----------------------|
| Python Base Station  |
| Telemetry Display    |
| Vehicle Controls     |
+----------+-----------+
            |
        USB Serial
            |
+----------v-----------+
| Base Station Arduino |
|      LoRa Radio      |
+----------+-----------+
            |
    Long Range LoRa Link
            |
+----------v-----------+
|     Radio Buoy       |
| RF + Video Relay     |
+----------+-----------+
            |
    Waterproof Tether
            |
+----------v-----------+
|     Submarine        |
| Arduino Controller   |
| Sensors              |
| ESCs                 |
| Camera               |
+----------------------+
```

---

# Hardware

## Submarine

### Controller

* Arduino Uno R4 WiFi

### Propulsion

* Three brushless motors
* Three electronic speed controllers (ESCs)

Configuration:

* Forward / Reverse
* Left / Right
* Up / Down

### Sensors

* LIS3DH Accelerometer
* MS5837 Depth Sensor
* Battery Voltage Monitor

### Lighting

* High-power LED floodlight

### Vision

* Analog FPV Camera (planned)

---

## Surface Radio Buoy

The radio buoy remains on the water surface while the submarine operates below.

Responsibilities:

* LoRa communication
* Video transmission
* Data tether to submarine

This architecture avoids RF signal loss underwater while allowing long-range communication above the surface.

---

## Base Station

The desktop application communicates with the surface buoy over USB LoRa module, with commands being set via Serial.

Responsibilities include:

* Sending movement commands
* Receiving telemetry
* Displaying vehicle status
* Logging sensor data
* Future graphical dashboard
* Future video display

---

# Firmware Architecture

```
Submarine/

main.cpp

motor.cpp
motor.h

rf.cpp
rf.h

sensors.cpp
sensors.h
```

## motor.cpp

Responsible for:

* ESC initialization
* Thruster control
* PWM generation

---

## rf.cpp

Responsible for:

* LoRa communication
* Command parsing
* Telemetry transmission
* Communication failsafe

---

## sensors.cpp

Responsible for:

* Battery monitoring
* IMU updates
* Depth sensor
* Sensor initialization

---

# Desktop Software

```
BaseStation/

main.py

config.py
radio.py
telemetry.py
controls.py
```

## radio.py

Handles communication with the base station USB LoRa.

## telemetry.py

Receives and parses telemetry packets.

## controls.py

Converts user inputs into vehicle movement commands.

## config.py

Stores configurable constants including:

* COM Port
* Baud Rate
* PWM Limits

---

# Communication Protocol

## Commands

The base station transmits control commands using a simple text protocol.

Example:

```
F:1500,T:1500,V:1500
```

Where:

| Field | Description       |
| ----- | ----------------- |
| F     | Forward Thruster  |
| T     | Turning Thruster  |
| V     | Vertical Thruster |

PWM values range from:

```
1000 = Full Reverse
1500 = Neutral
2000 = Full Forward
```

---

## Telemetry

Telemetry packets are transmitted in CSV format.

Example:

```
B:14.3,D:1.82,AX:0.02,AY:-0.03,AZ:9.81,P:2.4,R:-1.2
```

Fields include:

| Field | Description     |
| ----- | --------------- |
| B     | Battery Voltage |
| D     | Depth (m)       |
| AX    | Acceleration X  |
| AY    | Acceleration Y  |
| AZ    | Acceleration Z  |
| P     | Pitch           |
| R     | Roll            |

Future telemetry will include:

* Velocity
* Yaw
* Link Quality
* GPS Position (Surface Buoy)

---

# Safety Features

Current safety systems include:

* Communication timeout failsafe
* Automatic motor neutral after signal loss
* PWM output limiting

Planned additions include:

* Low battery return warning
* Emergency surface mode
* ESC fault monitoring

---

# Future Development

## Navigation

* Heading hold
* Depth hold
* Station keeping
* Waypoint following

## Computer Vision

* Underwater object detection
* Marker tracking
* Autonomous inspection

## Desktop Software

* Live telemetry dashboard
* Artificial horizon
* Depth gauge
* Vehicle status panel
* Video overlay
* Mission recording

## Hardware

* Custom PCB
* Brushless thruster upgrades
* Swappable battery modules

---

# Repository Structure

```
fpv-sub/

Submarine/
    main.cpp
    motor.cpp
    motor.h
    rf.cpp
    rf.h
    sensors.cpp
    sensors.h

Base Station/
    main.py
    config.py
    radio.py
    telemetry.py
    controls.py

README.md
```

