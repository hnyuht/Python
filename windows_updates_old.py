import win32com.client
import os

# Initialize the Windows Update Agent API
update_session = win32com.client.Dispatch("Microsoft.Update.Session")

# Create a search object to find available updates
searcher = update_session.CreateUpdateSearcher()

# Search for available updates
search_result = searcher.Search("IsInstalled=0 and Type='Software'")

# Check if any updates are available
if search_result.Updates.Count == 0:
    output = "Windows is up to date!"
else:
    # List the missing updates
    output = "The following updates are missing:\n"
    for update in search_result.Updates:
        output += f"{update.Title}\n"

# Create the output directory if it does not exist
output_dir = r"C:\Temp\XDR"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write the output to a file
output_path = os.path.join(output_dir, "windows_update_status.txt")
with open(output_path, "w") as f:
    f.write(output)
