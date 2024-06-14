import subprocess

def uninstall_java(version):
    try:
        uninstall_command = f'wmic product where "name like \'%Java%\' and (version like \'{version}%\')" call uninstall'
        result = subprocess.run(uninstall_command, shell=True, capture_output=True, text=True)
        if "ReturnValue = 0" in result.stdout:
            print(f"Successfully uninstalled Java version {version}")
        else:
            print(f"Failed to uninstall Java version {version}: {result.stdout}")
    except Exception as e:
        print(f"An error occurred while uninstalling Java version {version}: {str(e)}")

def main():
    versions_to_uninstall = [
        '6.0.51',  # Java 6 update 51 and higher
        '7.0.85',  # Java 7 update 85 and higher
        '8.0.211', # Java 8 update 211 and higher
    ]

    # Uninstall Java SE Development Kits (JDK) versions 9 through 16
    for version in range(9, 17):
        versions_to_uninstall.append(f'{version}.0')

    # Uninstall Java versions 11 through 16
    for version in range(11, 17):
        versions_to_uninstall.append(f'{version}.0')

    for version in versions_to_uninstall:
        uninstall_java(version)

if __name__ == "__main__":
    main()
