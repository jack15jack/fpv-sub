import threading


def parse_telemetry(line):

    data = {}

    try:

        parts = line.split(",")

        for part in parts:

            key, value = part.split(":")
            data[key] = float(value)

        return data

    except Exception:

        return None


def telemetry_loop(radio):

    while True:

        try:

            line = radio.read_line()

            if not line:
                continue

            data = parse_telemetry(line)

            if data is None:
                continue

            print("\n========== TELEMETRY ==========")

            print(f"Battery : {data.get('B',0):6.2f} V")
            print(f"Depth   : {data.get('D',0):6.2f} m")

            print(
                f"Accel   : "
                f"X={data.get('AX',0):6.2f}  "
                f"Y={data.get('AY',0):6.2f}  "
                f"Z={data.get('AZ',0):6.2f}"
            )

            print(f"Pitch   : {data.get('P',0):6.2f}°")
            print(f"Roll    : {data.get('R',0):6.2f}°")

        except Exception as e:

            print("Telemetry Error:", e)


def start_telemetry(radio):

    thread = threading.Thread(
        target=telemetry_loop,
        args=(radio,),
        daemon=True
    )

    thread.start()