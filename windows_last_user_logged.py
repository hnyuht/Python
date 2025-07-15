import subprocess

def get_current_logged_in_users():
    try:
        result = subprocess.run(
            ["quser"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_current_logged_in_users()
