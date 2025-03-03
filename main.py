from gpiozero import Button
import subprocess
import threading
import time
import os

# Button setup
button = Button(17)  # Update with your GPIO pin number

# Variable to track if the script is running
running = False

def run_rubber_duck_script():
    """
    Function to run the main script.
    """
    global running
    if running:
        print("The script is already running.")
        return

    running = True
    print("Rubber duck is awake and starting...")

    try:
        # Run the main script
        subprocess.run([
            "/home/finalproject/PycharmProjects/RubberDuck/.venv/bin/python",
            "/home/finalproject/PycharmProjects/RubberDuck/image2sound_new.py"
        ],
        
    )
    except Exception as e:
        print(f"Error running the script: {e}")

    print("Rubber duck is going back to sleep.")
    running = False


def button_press_handler():
    """
    Handles button press to start the script.
    """
    if not running:
        threading.Thread(target=run_rubber_duck_script).start()
    else:
        print("Rubber duck is already active.")


# Attach the button to the event
button.when_pressed = button_press_handler

# Notify the user
print("Rubber duck is idle. Waiting for button press...")
while True:
    time.sleep(1)  # Sleep to reduce CPU usage