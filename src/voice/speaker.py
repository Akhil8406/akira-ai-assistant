import pyttsx3


class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()

        # Speaking speed
        self.engine.setProperty("rate", 175)

        # Volume: 0.0 - 1.0
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()


if __name__ == "__main__":
    speaker = Speaker()

    speaker.speak("Hello. Systems are online. How can I help you?")
