import serial
import time
import threading

try:
    import pygame
    CONTROLLER_ENABLED = True
except:
    CONTROLLER_ENABLED = False

SERIAL_PORT = "COM5" # Change this based on the serial port used
BAUD_RATE = 9600

#pwm limits
PWM_MIN = 1000
PWM_MAX = 2000
PWM_NEUTRAL = 1500

# serial setup
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# telemetry parser5
def parse_telemetry(line):
    data = {}

    try:
        parts = line.strip().split(",")

        for part in parts:
            key, val = part.split(":")
            data[key] = float(val)

    except:
        return None

    return data

# telemetry thread
def telemetry_loop():
    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()

            if line:
                data = parse_telemetry(line)

                if data:
                    print(f"\n TELEMETRY")
                    print(f"Battery: {data.get('B', 0):.2f} V")
                    print(f"Depth: {data.get('D', 0):.2f} m")

                    print(f"Accel: X={data.get('AX', 0):.2f} "
                          f"Y={data.get('AY', 0):.2f} "
                          f"Z={data.get('AZ', 0):.2f}")
                    print(f"Pitch: {data.get('B', 0):.2f} V")
                    print(f"Roll: {data.get('B', 0):.2f} V")
        except Exception as e:
            print("Telemetry error", e)

# command sender
def send_command(f, t, v):
    cmd = f"F:{int(f)},T:{int(t)},V:{int(v)}\n"
    ser.write(cmd.encode())

# controller
def controller_loop():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No Controller found")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Controller connected:", joystick.get_name())

    while True:
        pygame.event.pump()

        #axes (may need tuning per controller)
        forward_axis    = -joystick.get_axis(1)     # left stick Y
        turn_axis       = joystick.get_axis(0)      # left stick X
        vertical_axis   = -joystick.get_axis(3)     # right stick Y

        # convert [-1, 1] -> [1000, 2000]
        f = PWM_NEUTRAL + forward_axis * 500
        t = PWM_NEUTRAL + turn_axis * 500
        v = PWM_NEUTRAL + vertical_axis * 500

        send_command(f, t, v)

        time.sleep(0.05) # 20 Hz

# keyboard fallback
def keyboard_loop():
    print("\nKeyboard control:")
    print("\nW/S = foward/back")
    print("\nA/D = left/right")
    print("\nR/F = up/down")
    print("\nQ = quit")

    f = PWM_NEUTRAL
    t = PWM_NEUTRAL
    v = PWM_NEUTRAL

    while True:
        key = input().lower()

        if key == "w":
            f = 1700
        elif key == "s":
            f = 1300
        else:
            f = PWM_NEUTRAL

        if key == "a":
            t = 1700
        elif key == "d":
            t = 1300
        else:
            t = PWM_NEUTRAL
        
        if key == "r":
            v = 1700
        elif key == "f":
            v = 1300
        else:
            v = PWM_NEUTRAL

        if key == "q":
            break

        send_command(f, t, v)

if __name__ == "__main__":
    print("Starting Base Station...")

    # start telemetry thread
    t_thread = threading.Thread(target=telemetry_loop, daemon=True)
    t_thread.start()

    # start control loop
    if CONTROLLER_ENABLED:
        controller_loop()
    else:
        keyboard_loop()

