import os
import shutil
import subprocess

def delete_files(directory):
    # Delete files
    deleted_files = []
    errors = []
    permissions_denied = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
            except OSError as e:
                if os.access(file_path, os.W_OK):
                    errors.append(f"Error deleting file: {file_path} - {e}")
                else:
                    permissions_denied.append(f"Permission denied: {file_path}")

    # Delete empty directories
    deleted_directories = []
    for root, _, _ in os.walk(directory, topdown=False):
        try:
            os.rmdir(root)
            deleted_directories.append(root)
        except OSError:
            pass

    return deleted_files, deleted_directories, errors, permissions_denied

# Specify the directory to delete files from
directory_path = r"C:\ProgramData\Cyvera\LocalSystem\Persistence"

# Call the function to delete files
deleted_files, deleted_directories, errors, permissions_denied = delete_files(directory_path)

# Stop the Cortex XDR agent service
cortex_xdr_agent_service_name = "cyserver.exe"
subprocess.call(["sc", "stop", cortex_xdr_agent_service_name])

# Start the Cortex XDR agent service
subprocess.call(["sc", "start", cortex_xdr_agent_service_name])

# Create the directory if it doesn't exist
output_directory = r"C:\Temp\XDR"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Write the output to a text file
output_file = os.path.join(output_directory, "db_output.txt")
with open(output_file, "w") as file:
    file.write("Deleted Files:\n")
    if deleted_files:
        for file_path in deleted_files:
            file.write(f"Deleted: {file_path}\n")
    else:
        file.write("No files deleted.\n")

    file.write("\nDeleted Directories:\n")
    if deleted_directories:
        for directory in deleted_directories:
            file.write(f"Deleted: {directory}\n")
    else:
        file.write("No directories deleted.\n")

    file.write("\nErrors:\n")
    if errors:
        for error in errors:
            file.write(error + "\n")
    else:
        file.write("No errors occurred during deletion.\n")

    file.write("\nPermissions Denied:\n")
    if permissions_denied:
        for denied in permissions_denied:
            file.write(denied + "\n")
    else:
        file.write("No permission issues encountered.\n")

print(f"Deletion completed. The output is written to '{output_file}'.")
