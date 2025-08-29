import serial
import time
from pynput.keyboard import Controller, Key

# --- Configuration ---
SERIAL_PORT = "COM6"  # TODO: change this to your COM port
BAUD_RATE = 115200
RECONNECT_DELAY_S = 2

# --- Pynput Key Mapping ---
# This dictionary maps the string from your serial device to the
# correct pynput key object or character. This makes the code
# much cleaner and easier to expand.
KEY_MAP = {
    "A": 'a',
    "B": 'b',
    "C": 'c',
    "D": 'd',
    "E": Key.space,
    # --- Add more mappings here! ---
    # "UP": Key.up,
    # "ENTER": Key.enter,
}


def process_serial_input(ser, keyboard_controller):
    """
    Reads a line from the serial port and simulates the corresponding keystroke.
    """
    try:
        line = ser.readline().decode("utf-8").strip()
        if not line:
            return  # Skip empty lines

        print(f"Received: {line}")

        # --- LOGIC FIX ---
        # Convert the received line to uppercase before looking it up in the KEY_MAP.
        # This makes the mapping case-insensitive and fixes the issue where
        # receiving 'a' doesn't match the key "A".
        key_to_press = KEY_MAP.get(line.upper())
        if key_to_press:
            print(f"  -> Simulating key: {key_to_press}")
            try:
                # Press and release the key
                keyboard_controller.press(key_to_press)
                keyboard_controller.release(key_to_press)
                print("  -> Keystroke sent successfully.")
            except Exception as e:
                # This error handling is crucial!
                print(f"  -> ERROR: Failed to send keystroke. Details: {e}")
                print("     This confirms a permission or software conflict issue with pynput.")
                print("     Make sure you are running this script as Administrator/sudo.")

        else:
            print(f"  -> No key mapping found for '{line}'")

    except UnicodeDecodeError:
        print("  -> Warning: Could not decode serial data. Check BAUD_RATE.")


def main():
    """
    Main loop to handle the serial connection and instantiate the controller.
    """
    print("--- Serial Pynput Keyboard Controller ---")
    print("Press Ctrl+C to exit.")
    
    # Instantiate the keyboard controller once
    keyboard_controller = Controller()

    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                print(f"✅ Connected to {SERIAL_PORT}")
                print("--> IMPORTANT: Click on the window you want to type in NOW!")
                while True:
                    process_serial_input(ser, keyboard_controller)

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