import subprocess

def get_ssh_version():
    try:
        # Use yum command to list installed openssh
        result = subprocess.run(['yum', 'list', 'installed', 'openssh'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            # Split the output by lines and find the line containing openssh
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Skip the header line
                if 'openssh' in line.lower():
                    parts = line.split()
                    return parts[-1]  # Last part should be the version
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
