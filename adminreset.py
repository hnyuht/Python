import subprocess

def reset_admin_password(username="Administrator", new_password="P@ssword123"):
    try:
        # PowerShell command to change the password
        powershell_command = f'net user {username} {new_password}'

        # Run the PowerShell command with elevated privileges
        result = subprocess.run(["powershell", "-Command", powershell_command], capture_output=True, text=True)

        # Check for errors
        if result.returncode == 0:
            print(f"Password for {username} successfully changed to {new_password}")
        else:
            print(f"Error changing password: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Reset the password
reset_admin_password()
