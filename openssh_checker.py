import subprocess

def get_ssh_version():
    try:
        # Use rpm command to query installed openssh package version
        result = subprocess.run(['rpm', '-q', '--queryformat', '%{VERSION}', 'openssh'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except subprocess.CalledProcessError:
        return None

# Get the version of openssh
ssh_version = get_ssh_version()

if ssh_version:
    print(f"The version of openssh installed is: {ssh_version}")
else:
    print("Failed to retrieve openssh version.")
