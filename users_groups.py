import os
import win32net
import win32security

def get_username():
    return os.environ.get('USERNAME')

def get_user_groups():
    user_groups = []
    user_info = win32net.NetUserGetInfo(None, get_username(), 2)
    if 'localgroup_memberships' in user_info:
        user_groups = user_info['localgroup_memberships']
    return user_groups

def get_user_roles():
    user_roles = []
    user_sid = win32security.LookupAccountName(None, get_username())[0]
    user_groups = get_user_groups()
    for group in user_groups:
        group_sid = win32security.LookupAccountName(None, group)[0]
        if win32security.IsWellKnownSid(group_sid, win32security.WinBuiltinAdministratorsSid):
            user_roles.append('Administrator')
        elif win32security.IsWellKnownSid(group_sid, win32security.WinBuiltinUsersSid):
            user_roles.append('User')
        else:
            user_roles.append(group)
    return user_roles

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    username = get_username()
    groups = get_user_groups()
    roles = get_user_roles()

    output_file_path = r'C:\temp\xdr\hostname_user_groups.txt'

    content = f"Windows Username: {username}\n"
    content += "Groups:\n"
    for group in groups:
        content += f"  - {group}\n"
    
    content += "\nRoles:\n"
    for role in roles:
        content += f"  - {role}\n"

    write_to_file(output_file_path, content)
    print(f"User groups and roles have been saved to: {output_file_path}")
