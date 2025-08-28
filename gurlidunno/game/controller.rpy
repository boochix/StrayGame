init python:
    import threading
    import serial

    # Change COM3 and baudrate to match your Arduino
    ser = serial.Serial('COM3', 9600, timeout=1)

    def send_to_arduino(scene, lives, hearts_flashing):
        msg = f"{scene},{lives},{int(hearts_flashing)}\n"
        ser.write(msg.encode())

    def listen_serial():
        while True:
            line = ser.readline().decode().strip()
            if line:
                # Example: send "a", "b", "c", "d" from Arduino
                if line in ["a", "b", "c", "d", "space"]:
                    renpy.invoke_in_thread(lambda: renpy.queue_event("arduino_" + line))

    threading.Thread(target=listen_serial, daemon=True).start()

# In your choice screen (screens.rpy), add key events for arduino input:
screen choice(items):
    default keymap = { "a": 0, "b": 1, "c": 2, "d": 3 }
    hbox:
        xalign 0.5
        yalign 0.9
        spacing gui.choice_spacing
        for i, item in enumerate(items):
            button:
                style "choice_button"
                action item.action
                text item.caption style "choice_button_text"
    # Keyboard keys
    for k, idx in keymap.items():
        if idx < len(items):
            key k action items[idx].action
            key "arduino_" + k action items[idx].action