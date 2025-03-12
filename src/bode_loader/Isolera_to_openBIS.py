# This script works as follows:
# Access an email account and filter emails by:
#   1. Sender - noreply@ethz.ch is the only email from which Isolera reports are sent
#   2. Date - Only emails from less than 60 days ago are checked
#   3. Subject - The subject of the messages must begin with Purification finishes
#   4. File extension - Only .pdf files are downloaded
# If the file does not already exist in the download directory, it will be downloaded

import imaplib
import email
import os
import json
import datetime
from email.utils import parsedate_to_datetime
from email.header import decode_header

config_path = '/Users/bodegroup/OpenBis/openbis-bode/config/config.json'

with open(config_path) as f:
    config = json.load(f)

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = config.get('email_account')
PASSWORD = config.get('password')
SEARCH_FROM = 'noreply@ethz.ch'
DOWNLOAD_FOLDER = '/Volumes/chab_loc_bode_s1/Instruments/Isolera/2025'

def connect_to_email():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select('inbox')
    return mail

def search_emails(mail):
    # Search for emails from a specific sender
    status, data = mail.search(None, f'(FROM "{SEARCH_FROM}")')
    email_ids = data[0].split()
    return email_ids

def decode_subject(subject):
    # Decode the subject in case it's encoded
    decoded_parts = decode_header(subject)
    subject_parts = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            part = part.decode(encoding if encoding else "utf-8")
        subject_parts.append(part)
    return ''.join(subject_parts)

def download_attachments(mail, email_ids):
    # Define the date threshold (approximately 2 months ago)
    two_months_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=60)
    
    skipped_emails = 0

    for e_id in email_ids:
        # Track if this email results in any downloads.
        downloaded_this_email = False

        status, data = mail.fetch(e_id, '(RFC822)')
        email_body = data[0][1]
        msg = email.message_from_bytes(email_body)

        # Parse and check the email date
        email_date_header = msg.get('Date')
        if email_date_header:
            try:
                msg_date = parsedate_to_datetime(email_date_header)
            except Exception:
                skipped_emails += 1
                continue
        else:
            skipped_emails += 1
            continue

        # Skip email if it's older than 2 months
        if msg_date < two_months_ago:
            skipped_emails += 1
            continue

        # Check if the subject starts with "Purification finished"
        subject = msg.get('Subject', '')
        decoded_subject = decode_subject(subject)
        if not decoded_subject.startswith("Purification finished"):
            skipped_emails += 1
            continue

        # Process attachments only if above conditions are met
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename and filename.lower().endswith('.pdf'):
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                if os.path.exists(filepath):
                    continue  # Skip if file already exists
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Downloaded: {filename}")
                downloaded_this_email = True

        # If no attachment was downloaded from this email, count it as skipped.
        if not downloaded_this_email:
            skipped_emails += 1

    return skipped_emails

def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    mail = connect_to_email()
    email_ids = search_emails(mail)
    if email_ids:
        skipped = download_attachments(mail, email_ids)
        print(f"Total emails skipped: {skipped}")
    else:
        print("No emails found from", SEARCH_FROM)
    mail.logout()

if __name__ == '__main__':
    main()
