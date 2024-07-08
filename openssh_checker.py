import subprocess

def check_package_installed(package_name, version):
    try:
        # Use yum command to check if package is installed
        result = subprocess.run(['yum', 'list', 'installed', f'{package_name}'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            # Check if the version is in the output
            return version in result.stdout
        else:
            return False
    except subprocess.CalledProcessError:
        return False

package_name = 'openssh.x86_64'
package_version = '8.7p1-38.e19_4.1'

if check_package_installed(package_name, package_version):
    print(f'{package_name} version {package_version} is installed.')
else:
    print(f'{package_name} version {package_version} is not installed.')
