from config import *


def keyboard_loop(radio):

    print("\n========== CONTROLS ==========\n")

    print("w : Forward")
    print("s : Reverse")
    print("a : Turn Left")
    print("d : Turn Right")
    print("r : Up")
    print("f : Down")
    print("x : Stop Motors")
    print("q : Quit\n")

    while True:

        forward = PWM_NEUTRAL
        turn = PWM_NEUTRAL
        vertical = PWM_NEUTRAL

        key = input("> ").lower().strip()

        if key == "w":
            forward += COMMAND_STEP

        elif key == "s":
            forward -= COMMAND_STEP

        elif key == "a":
            turn -= COMMAND_STEP

        elif key == "d":
            turn += COMMAND_STEP

        elif key == "r":
            vertical += COMMAND_STEP

        elif key == "f":
            vertical -= COMMAND_STEP

        elif key == "x":
            pass

        elif key == "q":

            radio.send_command(
                PWM_NEUTRAL,
                PWM_NEUTRAL,
                PWM_NEUTRAL
            )

            break

        else:

            print("Unknown Command")
            continue

        radio.send_command(
            forward,
            turn,
            vertical
        )