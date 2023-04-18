import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import re
from datetime import datetime
import time

# Set the credentials path
creds_path = 'credentials.json'
creds = Credentials.from_authorized_user_file(creds_path)

# Create a Gmail API client
service = build('gmail', 'v1', credentials=creds)

# Sanitize the sender and recipient addresses
def sanitize_address(address):
    # Replace period with [.]
    return address.replace('.', '[.]')

print("#" * 50) # Add separator line

# Get the subject and sender from user input
subject = input('Enter the subject of the email to search: ')
sender = input('Enter the sender email address to search: ')
print("#" * 50) # Add separator line

# Search for emails matching the given subject and sender
query = f"subject:{subject} from:{sender}"
result = service.users().messages().list(userId='me', q=query).execute()
print("#" * 50) # Add separator line

# Get a list of matching messages
messages = result.get('messages', [])
print("#" * 50) # Add separator line

# Check if any messages were found
if not messages:
    print('No emails found with the given criteria.')
else:
    print(f'{len(messages)} emails found with the given criteria.')
    print("#" * 50) # Add separator line

    # Display the list of messages and ask the user to confirm which messages to delete
    print('Messages:')
    for i, message in enumerate(messages):
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        subject = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'Subject')
        sender = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'From')
        timestamp = int(msg['internalDate'])/1000
        date_time = datetime.fromtimestamp(timestamp).strftime('%B %d, %Y %I:%M:%S %p')
        print(f'{i+1}. {subject} ({date_time})')
        time.sleep(2)  # add a 2-second delay after each request

    confirm_delete = input('Do you want to delete these emails? (y/n): ')
    delete_all = confirm_delete.lower() == 'y'

    # Loop through each message and delete the thread
    for message in messages:
        msg_id = message['id']
        service.users().messages().delete(userId='me', id=msg_id).execute()
        print(f'Email thread with message ID {msg_id} was successfully deleted.')
        
    # Sleep for 1 second to give the script some time to complete the operation
    time.sleep(1)
