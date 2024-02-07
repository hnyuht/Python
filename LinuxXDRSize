import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def format_size(size):
    # Define suffixes for kilobytes, megabytes, gigabytes, etc.
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    # Determine appropriate suffix and corresponding size
    for suffix in suffixes:
        if size < 1024:
            return f"{size:.2f} {suffix}"
        size /= 1024

folder_path = '/opt/traps'
folder_size = get_folder_size(folder_path)

print(f"The size of '{folder_path}' is: {format_size(folder_size)}")
