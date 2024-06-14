import subprocess
import re

def get_installed_java_versions():
    try:
        result = subprocess.run(['wmic', 'product', 'get', 'name,version'], capture_output=True, text=True)
        installed_products = result.stdout
        java_versions = []

        for line in installed_products.splitlines():
            if 'Java' in line:
                name_version = line.strip().split('  ')
                # Clean up the line and filter out unnecessary whitespace
                name_version = list(filter(None, name_version))
                if len(name_version) == 2:
                    name, version = name_version
                    java_versions.append((name.strip(), version.strip()))

        return java_versions
    except Exception as e:
        print(f"An error occurred while getting installed Java versions: {str(e)}")
        return []

def uninstall_java(name, version):
    try:
        uninstall_command = f'wmic product where "name=\'{name}\' and version=\'{version}\'" call uninstall'
        result = subprocess.run(uninstall_command, shell=True, capture_output=True, text=True)
        if "ReturnValue = 0" in result.stdout:
            print(f"Successfully uninstalled {name} version {version}")
        else:
            print(f"Failed to uninstall {name} version {version}: {result.stdout}")
    except Exception as e:
        print(f"An error occurred while uninstalling {name} version {version}: {str(e)}")

def main():
    versions_to_uninstall = [
        ('Java', '6.0.'),  # Java 6 update 51 and higher
        ('Java', '7.0.'),  # Java 7 update 85 and higher
        ('Java', '8.0.'),  # Java 8 update 211 and higher
    ]

    # Add Java SE Development Kits (JDK) versions 9 through 16
    for version in range(9, 17):
        versions_to_uninstall.append(('Java SE Development Kit', f'{version}.0'))

    # Add Java versions 11 through 16
    for version in range(11, 17):
        versions_to_uninstall.append(('Java', f'{version}.0'))

    installed_java_versions = get_installed_java_versions()
    for name, version in installed_java_versions:
        for pattern_name, pattern_version in versions_to_uninstall:
            if pattern_name in name and re.match(f'^{re.escape(pattern_version)}', version):
                uninstall_java(name, version)

if __name__ == "__main__":
    main()
