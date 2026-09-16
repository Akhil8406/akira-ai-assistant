import os
import subprocess
from urllib.parse import quote_plus


class BrowserController:
    def __init__(self):
        # Common Chrome installation locations
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]

        self.chrome_path = None

        for path in chrome_paths:
            if os.path.exists(path):
                self.chrome_path = path
                break

    def open_url(self, url):
        if self.chrome_path:
            subprocess.Popen([self.chrome_path, url])
            return True

        return False

    def open_google(self):
        if self.open_url("https://www.google.com"):
            return "Opening Google in Chrome."

        return "I couldn't find Google Chrome."

    def open_youtube(self):
        if self.open_url("https://www.youtube.com"):
            return "Opening YouTube in Chrome."

        return "I couldn't find Google Chrome."

    def open_gmail(self):
        if self.open_url("https://mail.google.com"):
            return "Opening Gmail in Chrome."

        return "I couldn't find Google Chrome."

    def search_google(self, query):
        query = query.strip()

        if not query:
            return "What would you like me to search for?"

        url = "https://www.google.com/search?q=" + quote_plus(query)

        if self.open_url(url):
            return f"Searching Google for {query}."

        return "I couldn't find Google Chrome."

    def search_youtube(self, query):
        query = query.strip()

        if not query:
            return "What would you like me to search for?"

        url = "https://www.youtube.com/results?search_query=" + quote_plus(query)

        if self.open_url(url):
            return f"Searching YouTube for {query}."

        return "I couldn't find Google Chrome."
