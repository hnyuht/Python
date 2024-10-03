import os
import re
from datetime import datetime

# Function to determine the log file location based on the distribution
def get_log_file():
    if os.path.exists("/var/log/auth.log"):  # For Ubuntu/Debian
        return "/var/log/auth.log"
    elif os.path.exists("/var/log/secure"):  # For RedHat/CentOS
        return "/var/log/secure"
    else:
        return None

# Function to parse the log file and get the most recent SSH user login
def get_recent_ssh_user(log_file):
    ssh_login_pattern = re.compile(r'Accepted\s+\w+\s+for\s+(\w+)\s+from\s+([\d.]+)\s+port')
    most_recent_user = None
    most_recent_time = None

    # Open and read the log file line by line
    with open(log_file, 'r') as file:
        for line in file:
            match = ssh_login_pattern.search(line)
            if match:
                user = match.group(1)
                # Extract the date from the log (assumed to be the first 15 characters)
                log_time_str = line[:15]
                log_time = datetime.strptime(log_time_str, "%b %d %H:%M:%S")
                log_time = log_time.replace(year=datetime.now().year)  # Add the current year

                # Keep track of the most recent user
                if most_recent_time is None or log_time > most_recent_time:
                    most_recent_time = log_time
                    most_recent_user = user

    return most_recent_user, most_recent_time

if __name__ == "__main__":
    log_file = get_log_file()
    
    if log_file:
        recent_user, recent_time = get_recent_ssh_user(log_file)
        
        if recent_user:
            print(f"The most recent SSH login was by user '{recent_user}' on {recent_time}")
        else:
            print("No SSH login found in the log file.")
    else:
        print("SSH log file not found on this system.")
