import shutil

# Path to McAfeeSystemExtensions in Applications folder
app_path = '/Applications/McAfeeSystemExtensions.app'

# Remove the application
try:
    shutil.rmtree(app_path)
    print("McAfeeSystemExtensions successfully uninstalled.")
except Exception as e:
    print(f"Error: {e}")
