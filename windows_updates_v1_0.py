import os
import platform
import win32com.client
import re

def get_kb_article_id(update_title):
    # Use regular expression to find the KB article ID in the update title
    match = re.search(r"KB\d+", update_title)
    return match.group() if match else "N/A"

def get_pending_windows_updates():
    try:
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        update_searcher = update_session.CreateUpdateSearcher()
        search_result = update_searcher.Search("IsInstalled=0")
        updates = search_result.Updates

        if not updates:
            return None

        return updates
    except Exception as e:
        print(f"Error while searching for updates: {e}")
        return None

def save_updates_to_txt(updates):
    if not updates:
        return

    host_name = platform.node()
    output_file_path = os.path.join("C:\\temp\\xdr", f"{host_name}_pending_windows_updates.txt")

    with open(output_file_path, "w") as file:
        for update in updates:
            file.write(f"Title: {update.Title}\n")
            file.write(f"Description: {update.Description}\n")
            file.write(f"KB Article: {get_kb_article_id(update.Title)}\n")
            file.write(f"Support URL: {update.SupportURL}\n")
            file.write(f"\n")

if __name__ == "__main__":
    updates = get_pending_windows_updates()
    save_updates_to_txt(updates)
