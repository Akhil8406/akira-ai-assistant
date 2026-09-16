from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailController:
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]

        self.credentials_file = self.project_root / "credentials.json"

        self.token_file = self.project_root / "token.json"

        self.service = None

    def connect(self):
        creds = None

        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.token_file), self.SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                if not self.credentials_file.exists():
                    raise FileNotFoundError(
                        "credentials.json was not found in the project root."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), self.SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open(self.token_file, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds, cache_discovery=False)

        return True

    # ==================================================
    # GET ONE MESSAGE
    # ==================================================

    def get_email_details(self, message_id):
        if self.service is None:
            self.connect()

        data = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            )
            .execute()
        )

        headers = data.get("payload", {}).get("headers", [])

        header_data = {header["name"].lower(): header["value"] for header in headers}

        return {
            "id": message_id,
            "from": header_data.get("from", "Unknown sender"),
            "subject": header_data.get("subject", "No subject"),
            "date": header_data.get("date", ""),
            "snippet": data.get("snippet", ""),
        }

    # ==================================================
    # RECENT EMAILS — MANUAL COMMAND
    # ==================================================

    def get_recent_emails(self, max_results=5):
        if self.service is None:
            self.connect()

        result = (
            self.service.users()
            .messages()
            .list(userId="me", maxResults=max_results)
            .execute()
        )

        messages = result.get("messages", [])

        emails = []

        for message in messages:
            emails.append(self.get_email_details(message["id"]))

        return emails

    # ==================================================
    # UNREAD EMAILS — BACKGROUND MONITOR
    # ==================================================

    def get_unread_emails(self, max_results=10):
        if self.service is None:
            self.connect()

        result = (
            self.service.users()
            .messages()
            .list(userId="me", q="is:unread", maxResults=max_results)
            .execute()
        )

        messages = result.get("messages", [])

        emails = []

        for message in messages:
            emails.append(self.get_email_details(message["id"]))

        return emails


if __name__ == "__main__":
    gmail = GmailController()

    print("\nConnecting AKIRA to Gmail...")

    emails = gmail.get_recent_emails(5)

    print(f"\nFound {len(emails)} recent emails.\n")

    for number, email in enumerate(emails, start=1):
        print("=" * 60)
        print(f"EMAIL {number}")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print(f"Preview: {email['snippet']}")
