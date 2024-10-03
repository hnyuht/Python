import re

def get_recent_ssh_user(log_file='/var/log/auth.log'):
    with open(log_file, 'r') as file:
        logs = file.readlines()

    # Regex pattern to match SSH logins
    ssh_login_pattern = r'sshd\[\d+\]: Accepted \w+ for (\w+)'
    
    for line in reversed(logs):
        match = re.search(ssh_login_pattern, line)
        if match:
            return match.group(1)

    return "No SSH login found."

# Example for Debian-based systems
recent_user = get_recent_ssh_user('/var/log/auth.log')
print(f"The most recent user to login via SSH: {recent_user}")

# For Red Hat-based systems, use '/var/log/secure'
# recent_user = get_recent_ssh_user('/var/log/secure')
