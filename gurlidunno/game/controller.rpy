init python:
    # Ensure the Ren'Py environment is set up to find PySerial
    import sys, os
    sys.path.append(os.path.join(config.renpy_base, "lib", "py3-windows-x86_64", "site-packages"))


    import serial, threading, time, os

    # --- custom logger ---
    def controller_log(msg):
        try:
            path = renpy.loader.transfn("controller_debug.log")
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except Exception as e:
            print("Logging failed:", e)

    ser = None
    stop_thread = False

    def read_serial():
        global ser, stop_thread
        while not stop_thread and ser:
            try:
                line = ser.readline().decode("utf-8").strip()
                if not line:
                    continue
                controller_log(f"Received: {line}")
                if line == "A":
                    renpy.queue_event("controller_A")
                elif line == "B":
                    renpy.queue_event("controller_B")
                elif line == "C":
                    renpy.queue_event("controller_C")
                elif line == "D":
                    renpy.queue_event("controller_D")
                elif line == "SPACE":
                    renpy.queue_event("controller_SPACE")
            except Exception as e:
                controller_log(f"Error: {e}")
                time.sleep(1)

    def connect_serial():
        global ser, stop_thread
        ports = ["COM3", "COM4", "COM5"]  # change if needed
        for port in ports:
            try:
                ser = serial.Serial(port, 9600, timeout=1)
                controller_log(f"✅ Serial connected on {port}")
                stop_thread = False
                t = threading.Thread(target=read_serial, daemon=True)
                t.start()
                return
            except Exception as e:
                controller_log(f"Failed on {port}: {e}")
        controller_log("❌ No serial ports available.")

    def cleanup_controller():
        global ser, stop_thread
        stop_thread = True
        if ser:
            ser.close()
            controller_log("🔌 Serial closed.")
            ser = None

    config.quit_callbacks.append(cleanup_controller)

    connect_serial()
