import subprocess

def uninstall_filezilla():
    try:
        # Path to FileZilla uninstaller
        uninstaller_path = r"C:\Program Files\FileZilla FTP Client\uninstall.exe"
        
        # Run the uninstaller with the /S flag for silent uninstallation
        subprocess.run([uninstaller_path, "/S"], check=True)
        print("FileZilla has been successfully uninstalled.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("FileZilla uninstallation failed.")

# Run the uninstall function
uninstall_filezilla()
