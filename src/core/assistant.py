from src.voice.listener import Listener
from src.voice.speaker import Speaker

from src.tools.windows import WindowsController
from src.tools.browser import BrowserController
from src.tools.email import GmailController

from src.brain.agent import AkiraBrain


class Assistant:
    def __init__(self):
        # ==========================================
        # VOICE
        # ==========================================

        self.listener = Listener()
        self.speaker = Speaker()

        # ==========================================
        # LOCAL AI BRAIN
        # ==========================================

        self.brain = AkiraBrain()

        # ==========================================
        # LAPTOP TOOLS
        # ==========================================

        self.windows = WindowsController()
        self.browser = BrowserController()

        # ==========================================
        # GMAIL
        # ==========================================

        self.gmail = GmailController()

    # ==================================================
    # FAST MANUAL EMAIL CHECK
    # ==================================================

    def check_emails(self):
        try:
            print("📧 Checking Gmail...")

            # Only fetch the latest 3 emails.
            # We intentionally DO NOT use Ollama here
            # because that makes a simple inbox check slow.

            emails = self.gmail.get_recent_emails(3)

            if not emails:
                return "You don't have any recent emails."

            parts = []

            for email in emails:
                sender = email["from"].strip()
                subject = email["subject"].strip()

                # Example:
                #
                # Google <no-reply@google.com>
                #
                # becomes:
                #
                # Google

                if "<" in sender:
                    sender = sender.split("<")[0].strip()

                # Remove quotes around sender names
                sender = sender.strip('"')

                parts.append(f"From {sender}: {subject}")

            response = f"You have {len(emails)} recent emails. " + ". ".join(parts)

            return response

        except Exception as error:
            print(f"❌ Gmail error: {error}")

            return "I couldn't access your Gmail right now."

    # ==================================================
    # EMAIL IMPORTANCE CLASSIFIER
    # ==================================================

    def classify_email(self, email):
        prompt = f"""
Classify this email.

Return ONLY one word:

IMPORTANT

or

IGNORE

IMPORTANT includes:

- university emails
- professors
- university administration
- exam information
- application updates
- job applications
- interview invitations
- recruiter messages
- employment contracts
- appointments
- deadlines
- immigration
- government
- banking problems
- payment issues
- account security alerts
- important personal messages

IGNORE includes:

- advertisements
- newsletters
- generic job recommendations
- marketing emails
- promotions
- shopping emails
- social media notifications
- automated commercial digests
- generic job alert newsletters

Sender:
{email["from"]}

Subject:
{email["subject"]}

Preview:
{email["snippet"]}
"""

        try:
            result = self.brain.ask(prompt).strip().upper()

            return result.startswith("IMPORTANT")

        except Exception as error:
            print(f"❌ Email classification error: {error}")

            return False

    # ==================================================
    # CREATE AUTOMATIC EMAIL VOICE ALERT
    # ==================================================

    def create_email_alert(self, email):
        prompt = f"""
Create a very short spoken notification for
this important email.

Rules:

- Maximum two short sentences.
- Mention the sender.
- Explain what the email appears to be about.
- Do not invent information.
- Do not read the entire email.
- Make it sound natural when spoken by AKIRA.

Sender:
{email["from"]}

Subject:
{email["subject"]}

Preview:
{email["snippet"]}
"""

        try:
            alert = self.brain.ask(prompt).strip()

            return alert

        except Exception as error:
            print(f"❌ Email alert generation error: {error}")

            return "You have received a new important email."

    # ==================================================
    # COMMAND PROCESSOR
    # ==================================================

    def process_command(self, command):
        command = command.lower().strip()

        # ==========================================
        # AKIRA IDENTITY
        # ==========================================

        if "your name" in command or "who are you" in command:
            return "My name is Akira, your personal desktop assistant."

        # ==========================================
        # FAST GMAIL CHECK
        # ==========================================

        elif (
            "check my emails" in command
            or "check my email" in command
            or "check emails" in command
            or "check email" in command
            or "read my emails" in command
            or "read my email" in command
            or "latest emails" in command
            or "recent emails" in command
        ):
            return self.check_emails()

        # ==========================================
        # OPEN GMAIL
        # ==========================================

        elif "open gmail" in command:
            return self.browser.open_gmail()

        # ==========================================
        # GOOGLE SEARCH
        # ==========================================

        elif command.startswith("search google for "):
            query = command.replace("search google for ", "", 1)

            return self.browser.search_google(query)

        elif command.startswith("google "):
            query = command.replace("google ", "", 1)

            return self.browser.search_google(query)

        # ==========================================
        # OPEN GOOGLE
        # ==========================================

        elif "open google" in command:
            return self.browser.open_google()

        # ==========================================
        # YOUTUBE SEARCH
        # ==========================================

        elif command.startswith("search youtube for "):
            query = command.replace("search youtube for ", "", 1)

            return self.browser.search_youtube(query)

        # ==========================================
        # OPEN YOUTUBE
        # ==========================================

        elif "open youtube" in command:
            return self.browser.open_youtube()

        # ==========================================
        # OPEN CHROME
        # ==========================================

        elif "open chrome" in command:
            return self.windows.open_chrome()

        # ==========================================
        # OPEN VS CODE
        # ==========================================

        elif (
            "open visual studio code" in command
            or "open vs code" in command
            or "open vscode" in command
        ):
            return self.windows.open_vscode()

        # ==========================================
        # OPEN FILE EXPLORER
        # ==========================================

        elif "open file explorer" in command or "open explorer" in command:
            return self.windows.open_explorer()

        # ==========================================
        # OPEN WINDOWS SETTINGS
        # ==========================================

        elif "open settings" in command:
            return self.windows.open_settings()

        # ==========================================
        # OPEN CALCULATOR
        # ==========================================

        elif "open calculator" in command or "open the calculator" in command:
            return self.windows.open_calculator()

        # ==========================================
        # EVERYTHING ELSE → LOCAL AI
        # ==========================================

        else:
            print("🧠 Sending request to AKIRA local AI...")

            return self.brain.ask(command)
