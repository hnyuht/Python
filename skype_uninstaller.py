import subprocess
import os

def uninstall_skype():
    try:
        # Specify the Skype package name or wildcard pattern
        package_name = "Microsoft.SkypeApp*"

        # Execute the PowerShell command to uninstall the Skype app
        subprocess.run(['C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe',
                        '-Command', f'Get-AppxPackage -AllUsers | Where-Object {{$_.Name -like "{package_name}"}} | ForEach-Object {{Remove-AppxPackage -Package $_.PackageFullName}}'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Specify the path to the Skype uninstaller
        skype_uninstaller_path = r"C:\Program Files (x86)\Microsoft\Skype for Desktop\unins000.exe"

        # Check if the uninstaller file exists
        if os.path.exists(skype_uninstaller_path):
            # Execute the Skype uninstaller with appropriate arguments
            subprocess.run([skype_uninstaller_path, "/silent"])

    except Exception as e:
        print("An error occurred while uninstalling Skype:", str(e))

if __name__ == '__main__':
    uninstall_skype()
