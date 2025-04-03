from typing import Dict, Any
import argparse
import os
import logging
from mcp.server import FastMCP
from mcp.types import TextContent
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GmailService:
    """Service for interacting with Gmail API"""
    
    def __init__(self, creds_file_path: str, token_path: str):
        """Initialize the Gmail service with credentials"""
        self.creds_file_path = creds_file_path
        self.token_path = token_path
        self.scopes = ['https://www.googleapis.com/auth/gmail.send']
        self.service = None
        
        print("Initializing GmailService with creds file:", creds_file_path)
        self.token = self._get_token()
        self.service = self._init_service()
        print("GmailService initialized")
    
    def _get_token(self) -> Credentials:
        """Get a valid token for Gmail API access"""
        print("Loading token from file")
        creds = None
        
        if os.path.exists(self.token_path) and os.path.getsize(self.token_path) > 0:
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
                print("Token loaded from file")
            except Exception as e:
                print("Error loading token:", e)
                creds = None
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token")
                creds.refresh(Request())
            else:
                print("Getting new token")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.creds_file_path, self.scopes)
                    creds = flow.run_local_server(port=0)
                    print("New token obtained")
                except Exception as e:
                    print("Error getting new token:", e)
                    raise
        
        try:
            with open(self.token_path, 'w') as token_file:
                token_file.write(creds.to_json())
            print("Token saved to", self.token_path)
        except Exception as e:
            print("Error saving token:", e)
        
        return creds
    
    def _init_service(self):
        """Initialize the Gmail API service"""
        try:
            service = build('gmail', 'v1', credentials=self.token)
            print("Gmail API service initialized")
            return service
        except Exception as e:
            print("Error initializing Gmail API service:", e)
            raise
    
    def send_email_with_attachment(self, recipient_id: str, subject: str, message: str, attachment_path: str) -> Dict[str, Any]:
        """Send an email with an attachment to a recipient"""
        try:
            # Create the message
            message_obj = MIMEMultipart()
            message_obj['to'] = recipient_id
            message_obj['subject'] = subject
            
            # Add the message body
            msg = MIMEText(message, 'plain')
            message_obj.attach(msg)
            
            # Add the attachment
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype=os.path.splitext(attachment_path)[1][1:])
                    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                    message_obj.attach(attachment)
            else:
                print("Attachment file not found:", attachment_path)
            
            # Encode the message
            raw_message = base64.urlsafe_b64encode(message_obj.as_bytes()).decode('utf-8')
            
            # Send the message
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            print("Email with attachment sent successfully to", recipient_id)
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Email with attachment sent successfully to {recipient_id}. Message ID: {sent_message.get('id')}"
                    )
                ]
            }
        except Exception as e:
            print("Error sending email with attachment:", e)
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Error sending email with attachment: {str(e)}"
                    )
                ]
            }

def main(creds_file_path: str, token_path: str):
    """Main function to run the Gmail MCP server"""
    # Initialize the Gmail service
    gmail_service = GmailService(creds_file_path, token_path)
    
    # Initialize the MCP server
    mcp = FastMCP("Gmail")
    
    # Define the list_tools function
    @mcp.tool()
    def list_tools() -> Dict[str, Any]:
        """List all available tools"""
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Available tools: send_email_with_attachment"
                )
            ]
        }
    
    # Define the send_email_with_attachment function
    @mcp.tool()
    def send_email_with_attachment(recipient_id: str, subject: str, message: str, attachment_path: str) -> Dict[str, Any]:
        """Send an email with an attachment to a recipient"""
        return gmail_service.send_email_with_attachment(recipient_id, subject, message, attachment_path)
    
    # Run the MCP server
    mcp.run(transport="stdio")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gmail MCP Server")
    parser.add_argument("--creds-file-path", required=True, help="Path to the credentials file")
    parser.add_argument("--token-path", required=True, help="Path to the token file")
    args = parser.parse_args()
    
    main(args.creds_file_path, args.token_path) 