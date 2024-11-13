import subprocess

def create_admin_user(username="Administrator1", password="P@ssword123"):
    try:
        # Command to create a new user with the specified username and password
        create_user_cmd = f'New-LocalUser -Name {username} -Password (ConvertTo-SecureString "{password}" -AsPlainText -Force)'
        
        # Command to add the new user to the Administrators group
        add_to_admin_group_cmd = f'Add-LocalGroupMember -Group "Administrators" -Member {username}'

        # Run the PowerShell command to create the user
        result_create_user = subprocess.run(["powershell", "-Command", create_user_cmd], capture_output=True, text=True)
        if result_create_user.returncode == 0:
            print(f"User '{username}' created successfully.")
        else:
            print(f"Error creating user: {result_create_user.stderr}")
            return

        # Run the PowerShell command to add the user to the Administrators group
        result_add_to_group = subprocess.run(["powershell", "-Command", add_to_admin_group_cmd], capture_output=True, text=True)
        if result_add_to_group.returncode == 0:
            print(f"User '{username}' added to the Administrators group successfully.")
        else:
            print(f"Error adding user to Administrators group: {result_add_to_group.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Create a new admin user with the specified username and password
create_admin_user()
