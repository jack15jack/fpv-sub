import serial
import time

from config import *


class Radio:

    def __init__(self):
        self.ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=SERIAL_TIMEOUT
        )

        time.sleep(2)

        print(f"Connected to {SERIAL_PORT}")

    def read_line(self):
        return self.ser.readline().decode(
            errors="ignore"
        ).strip()

    def send_command(self, forward, turn, vertical):
        forward = max(PWM_MIN, min(PWM_MAX, forward))
        turn = max(PWM_MIN, min(PWM_MAX, turn))
        vertical = max(PWM_MIN, min(PWM_MAX, vertical))

        packet = (
            f"F:{forward},"
            f"T:{turn},"
            f"V:{vertical}\n"
        )

        self.ser.write(packet.encode())

    def close(self):
        self.ser.close()