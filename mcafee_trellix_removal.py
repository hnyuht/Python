import subprocess

def uninstall_mcafee():
    paths = [
        r'"c:\Program Files\McAfee\Agent\x86\frminst.exe" /forceuninstall',
        r'"c:\Program Files\McAfee\Common Framework\x86\frminst.exe" /forceuninstall'
    ]
    for path in paths:
        try:
            subprocess.run(path, shell=True, check=True)
            print(f"McAfee uninstallation using {path} successful.")
        except subprocess.CalledProcessError:
            print(f"McAfee uninstallation using {path} failed.")

if __name__ == "__main__":
    uninstall_mcafee()
