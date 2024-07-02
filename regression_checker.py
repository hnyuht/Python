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
        print(f"Error fetching OpenSSH version: {e}")
        return None

def is_vulnerable(version):
    try:
        major, minor_patch = version.split('.')[:2]
        minor, patch = minor_patch.split('p')
        major = int(major)
        minor = int(minor)
        patch = int(patch)

        if major < 4 or (major == 4 and minor < 4):
            return True
        elif major == 4 and minor == 4 and patch == 0:
            return False
        elif (4 <= major < 8) or (major == 8 and minor < 5):
            return False
        elif (major == 8 and minor == 5 and patch == 0):
            return True
        elif 8 <= major < 9 or (major == 9 and minor < 8):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error parsing version: {e}")
        return False

def main():
    version = get_openssh_version()
    if version:
        print(f"OpenSSH version: {version}")
        if is_vulnerable(version):
            print("This version of OpenSSH is vulnerable.")
        else:
            print("This version of OpenSSH is not vulnerable.")
    else:
        print("Could not determine OpenSSH version.")

if __name__ == "__main__":
    main()
