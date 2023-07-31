import os

def reboot_windows():
    try:
        os.system("shutdown /r /t 0")
    except Exception as e:
        print("An error occurred while trying to reboot Windows:", e)

if __name__ == "__main__":
    print("Rebooting Windows...")
    reboot_windows()
