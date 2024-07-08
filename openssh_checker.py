import subprocess

def get_ssh_version():
    try:
        # Use yum command to list installed openssh
        result = subprocess.run(['yum', 'list', 'installed', 'openssh'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            # Split the output by lines
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'openssh' in line.lower():
                    # Extract version from the line
                    parts = line.split()
                    version = parts[-1]
                    return version
            return None
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
