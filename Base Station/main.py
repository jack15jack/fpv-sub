from radio import Radio
from telemetry import start_telemetry
from controls import keyboard_loop


def main():

    radio = Radio()

    start_telemetry(radio)

    keyboard_loop(radio)

    radio.close()

    print("Disconnected")


if __name__ == "__main__":
    main()