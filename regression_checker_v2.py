import subprocess
import re

def get_openssh_version():
    try:
        result = subprocess.run(['ssh', '-V'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        version_output = result.stderr.strip()  # Version info is usually in stderr
        version_match = re.search(r'OpenSSH_(\d+\.\d+p\d+)', version_output)
        if version_match:
            return version_match.group(1)
        else:
            return None
    except Exception as e:
        return f"Error fetching OpenSSH version: {e}"

def is_vulnerable(version):
    try:
        major, minor_patch = version.split('.')[:2]
        minor, patch = minor_patch.split('p')
        major = int(major)
        minor = int(minor)
        patch = int(patch)

        if major < 4 or (major == 4 and minor < 4):
            return True, "Vulnerable unless patched for CVE-2006-5051 and CVE-2008-4109"
        elif major == 4 and minor == 4 and patch == 0:
            return False, "Not vulnerable"
        elif (4 <= major < 8) or (major == 8 and minor < 5):
            return False, "Not vulnerable"
        elif (major == 8 and minor == 5 and patch == 0):
            return True, "Vulnerable"
        elif 8 <= major < 9 or (major == 9 and minor < 8):
            return True, "Vulnerable"
        else:
            return False, "Not vulnerable"
    except Exception as e:
        return False, f"Error parsing version: {e}"

def check_login_grace_time():
    config_file_path = "/etc/ssh/sshd_config"
    try:
        with open(config_file_path, 'r') as file:
            config_content = file.read()
        match = re.search(r'^\s*LoginGraceTime\s+(\d+)', config_content, re.MULTILINE)
        if match:
            value = int(match.group(1))
            if value == 0:
                return True, "LoginGraceTime is set to 0, which mitigates the vulnerability but exposes sshd to DoS risks."
            else:
                return False, f"LoginGraceTime is set to {value}, which does not mitigate the vulnerability."
        else:
            return False, "LoginGraceTime is not set in the sshd_config file."
    except FileNotFoundError:
        return False, f"Configuration file {config_file_path} not found."
    except Exception as e:
        return False, f"Error checking LoginGraceTime: {e}"

def check_rpm_installed_and_hash():
    rpm_name = "openssh-8.7p1-38.el9_4.1.x86_64"
    expected_hash = "c795537c8aade8f8b4018f8deb14572779501265cea929ecb509f22f4598e7a2"
    
    try:
        rpm_check = subprocess.run(['rpm', '-q', rpm_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if rpm_check.returncode != 0:
            return False, "RPM package is not installed."

        rpm_info = subprocess.run(['rpm', '-ql', rpm_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        installed_files = rpm_info.stdout.strip().split('\n')

        for file in installed_files:
            if re.search(r'openssh.*\.rpm$', file):
                hash_check = subprocess.run(['sha256sum', file], stdout=subprocess.PIPE, text=True)
                actual_hash = hash_check.stdout.split()[0]
                if actual_hash == expected_hash:
                    return True, "RPM is installed and hash matches."
                else:
                    return False, f"RPM is installed but hash does not match (expected {expected_hash}, got {actual_hash})."
        
        return False, "RPM is installed but no matching files found for hash verification."
    except Exception as e:
        return False, f"Error checking RPM package and hash: {e}"

def main():
    output = []
    
    version = get_openssh_version()
    if version:
        output.append(f"OpenSSH version: {version}")
        vulnerable, message = is_vulnerable(version)
        if vulnerable:
            output.append(f"This version of OpenSSH is vulnerable. {message}")
            mitigated, mitigation_message = check_login_grace_time()
            output.append(f"Mitigation status: {mitigation_message}")
        else:
            output.append(f"This version of OpenSSH is not vulnerable. {message}")
    else:
        output.append("Could not determine OpenSSH version.")

    rpm_installed, rpm_message = check_rpm_installed_and_hash()
    output.append(f"RPM check: {rpm_message}")

    print("\n".join(output))

if __name__ == "__main__":
    main()
