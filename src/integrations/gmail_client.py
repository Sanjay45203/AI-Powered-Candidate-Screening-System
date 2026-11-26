import os, base64
from pathlib import Path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

class GmailClient:
    def __init__(self):
        token_path = Path(os.getenv("GOOGLE_TOKEN_FILE", "token.json"))
        client_path = Path(os.getenv("GOOGLE_OAUTH_CLIENT_FILE", "credentials.json"))
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES) if token_path.exists() else None
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        if not creds or not creds.valid:
            if not client_path.exists():
                raise FileNotFoundError(f"OAuth client file not found: {client_path}")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_path), SCOPES)
            creds = flow.run_local_server(port=0)
            token_path.write_text(creds.to_json(), encoding="utf-8")
        self.service = build("gmail", "v1", credentials=creds)

    def send_email(self, to: str, subject: str, body: str) -> dict:
        message = MIMEText(body)
        message["to"], message["subject"] = to, subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return self.service.users().messages().send(userId="me", body={"raw": raw}).execute()
