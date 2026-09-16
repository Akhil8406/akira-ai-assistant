import os
import subprocess
import webbrowser


class WindowsController:
    def open_chrome(self):
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                return "Opening Chrome."

        # Fallback to default browser
        webbrowser.open("https://www.google.com")
        return "Opening your browser."

    def open_vscode(self):
        try:
            subprocess.Popen(["code"], shell=True)
            return "Opening Visual Studio Code."

        except Exception:
            return "I couldn't open Visual Studio Code."

    def open_explorer(self):
        subprocess.Popen(["explorer"])
        return "Opening File Explorer."

    def open_settings(self):
        os.startfile("ms-settings:")
        return "Opening Settings."

    def open_calculator(self):
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."


if __name__ == "__main__":
    controller = WindowsController()

    print(controller.open_calculator())
