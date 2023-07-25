import os

def list_items_in_path(path):
    return os.listdir(path)

def list_items_to_file(file_path, items_list):
    with open(file_path, 'w') as file:
        for item in items_list:
            file.write(item + '\n')

if __name__ == "__main__":
    # Specify the paths to list items from
    paths_to_list = [
        (r'C:\Program Files', 'ProgramFiles'),
        (r'C:\Program Files (x86)', 'ProgramFiles(x86)')
    ]

    # Create the output directory if it doesn't exist
    output_directory = r'C:\temp\XDR'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Get items from each path and save them to separate files
    for path, name in paths_to_list:
        items_in_path = list_items_in_path(path)
        output_file_path = os.path.join(output_directory, f'{name}_items.txt')
        list_items_to_file(output_file_path, items_in_path)
        print(f"Items listed in '{output_file_path}'")
