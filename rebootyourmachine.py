import time
import os
import sys

def countdown(minutes=5):
    seconds = minutes * 60
    while seconds >= 0:
        mins, secs = divmod(seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        # Print on the same line, overwriting previous time
        sys.stdout.write(f"\rRestarting in {time_str} - Please save your work.")
        sys.stdout.flush()
        time.sleep(1)
        seconds -= 1
    print("\nTime's up! Restarting now.")
    restart_system()

def restart_system():
    # Windows command to restart the machine
    os.system("shutdown /r /t 0")

# Message to display initially
print("Due to a security update, we need to restart your machine.")
print("Please save all your work and restart manually, or wait for the timer.")
print("The system will automatically restart in 5 minutes.\n")

# Start the countdown
countdown(5)
