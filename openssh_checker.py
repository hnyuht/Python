import subprocess

def check_package_installed(package_name, version):
    try:
        # Use yum command to list installed packages matching 'openssh'
        result = subprocess.run(['yum', 'list', 'installed', package_name], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            # Check if the version is in the output
            return version in result.stdout.strip()
        else:
            return False
    except subprocess.CalledProcessError:
        return False

# Define the package name and version to check
package_name = 'openssh'
package_versions = ['8.7p1-38.el9_4.1', 'openssh-8.7p1-38.el9_4.1']

# Check each version
found = False
for version in package_versions:
    if check_package_installed(package_name, version):
        print(f'{package_name} version {version} is installed.')
        found = True
        break

if not found:
    print(f'{package_name} versions {", ".join(package_versions)} are not installed.')
