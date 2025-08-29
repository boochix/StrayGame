import keyboard
import time
import sys

def test_keyboard_permissions():
    """
    A simple diagnostic script to test if the keyboard library can send keystrokes.
    """
    print("--- Keyboard Library Permission Test ---")
    print("\nThis script will try to type a message in 5 seconds.")
    print("IMPORTANT: After starting, you MUST click on a different window")
    print("(like a text editor or Notepad) to make it active.")
    print("-" * 40)

    for i in range(5, 0, -1):
        # Print countdown on the same line
        sys.stdout.write(f"\rTyping in {i}...")
        sys.stdout.flush()
        time.sleep(1)

    print("\n\nAttempting to type 'hello world'.")

    try:
        # Use a simple write command to test functionality
        keyboard.write("hello world")
        print("✅ SUCCESS: The script was able to send keystrokes.")
        print("If this worked, the issue might be related to the main script's logic.")
        print("Try the updated serial_keyboard_controller.py script.")

    except Exception as e:
        print(f"\n❌ ERROR: Failed to send keystrokes. Details: {e}")
        print("This confirms that something on your system is blocking the keyboard library,")
        print("even with administrator rights.")
        print("\nPossible Causes:")
        print("  - Aggressive antivirus or anti-malware software.")
        print("  - Specific security software from a device manufacturer (e.g., Dell, HP).")
        print("  - Anti-cheat software for games if it's running in the background.")
        print("\nNext Steps:")
        print("  - Try temporarily disabling your antivirus/security software to see if it's the cause.")
        print("  - Check for any other security-related programs that might be running.")

test_keyboard_permissions()