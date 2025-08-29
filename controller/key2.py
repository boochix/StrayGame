import serial
import time
import keyboard

# --- Configuration ---
# TODO: Change this to the correct COM port for your device.
SERIAL_PORT = "COM6"
BAUD_RATE = 115200
RECONNECT_DELAY_S = 2  # Time in seconds to wait before trying to reconnect

# This dictionary maps the string received from the serial device
# to the key(s) that should be pressed.
# Using a dictionary makes it much easier to add or change keys without
# needing a long chain of if/elif statements.
#
# You can find a list of all possible key names here:
# https://github.com/boppreh/keyboard#keyboard.send
KEY_MAP = {
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "SPACE": "space",
    # --- Add more custom mappings below! ---
    # Example: Map "UP" from serial to the up arrow key
    # "UP": "up",
    # Example: Map "CTRL_S" from serial to a key combination
    # "CTRL_S": "ctrl+s",
}


def process_serial_input(ser):
    """
    Reads lines from the serial connection and triggers keyboard events.
    """
    try:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            return  # Skip empty lines

        print(f"Received: {line}")

        # Look up the received command in our KEY_MAP
        key_to_press = KEY_MAP.get(line)

        if key_to_press:
            keyboard.send(key_to_press)
            print(f"  -> Simulated key press: '{key_to_press}'")
        else:
            print(f"  -> No keyboard mapping found for '{line}'")

    except UnicodeDecodeError:
        # This can happen if the serial data is garbled
        print("  -> Warning: Could not decode serial data.")


def main():
    """
    Main loop to handle serial connection and reconnection.
    """
    print("--- Serial Keyboard Controller ---")
    print("Press Ctrl+C to exit.")

    while True:
        try:
            # The 'with' statement ensures the serial port is properly closed
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                print(f"✅ Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
                while True:
                    process_serial_input(ser)

        except serial.SerialException:
            print(f"⚠  Serial port '{SERIAL_PORT}' not found or disconnected.")
            print(f"   Retrying in {RECONNECT_DELAY_S} seconds...")
            time.sleep(RECONNECT_DELAY_S)

        except KeyboardInterrupt:
            print("\n🛑 Program terminated by user.")
            break

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break


if _name_ == "_main_":
    main()