import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import re
from datetime import datetime
import time

# Set the credentials path
creds = Credentials.from_authorized_user_file('credentials.json')

# Create a Gmail API client
service = build('gmail', 'v1', credentials=creds)

# Sanitize the sender and recipient addresses
def sanitize_address(address):
    # Replace period with [.]
    return address.replace('.', '[.]')

# Get the subject and sender from user input
subject = input('Enter the subject of the email to search: ')
sender = input('Enter the sender email address to search: ')
print("#" * 50) # Add separator line

# Search for emails matching the given subject and sender
query = f"subject:{subject} from:{sender}"
result = service.users().messages().list(userId='me', q=query).execute()

# Get a list of matching messages
messages = result.get('messages', [])

# Check if any messages were found
if not messages:
    print('No emails found with the given subject and sender.')
else:
    print(f'{len(messages)} emails found with the given subject and sender.')
    
    # Loop through each message and delete it
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        subject = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'Subject')
        sender = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'From')
        body = None
        attachment_name = None
        
        # Get the message body and attachment name if present
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif 'attachmentId' in part:
                    attachment = service.users().messages().attachments().get(
                        userId='me', messageId=message['id'], id=part['attachmentId']).execute()
                    attachment_data = attachment['data']
                    attachment_name = part['filename']
                
        # Sanitize the sender and recipient addresses
        sender = sanitize_address(sender)
        to = [sanitize_address(header['value']) for header in msg['payload']['headers'] if header['name'] == 'To']
        cc = [sanitize_address(header['value']) for header in msg['payload']['headers'] if header['name'] == 'Cc']

        # Get the date and time of the message
        timestamp = int(msg['internalDate'])/1000
        date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        print(f"Sender: {sender}")
        print(f"To: {to}")
        print(f"Cc: {cc}")
        print(f"Subject: {subject}")
        print(f"Date and Time: {date_time}")
        if body:
            print(f"Body: {body}")
        if attachment_name:
            print(f"Attachment Name: {attachment_name}")

        # Sleep for 1 second to give the script some time to complete
