import speech_recognition as sr


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Better settings for normal speech
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

        print("🎙️ AKIRA microphone initializing...")

        # Initial calibration
        with self.microphone as source:

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1.5
            )

        print(
            f"✅ Microphone ready. "
            f"Threshold: {self.recognizer.energy_threshold}"
        )

    def listen(self, silent=False):

        try:

            with self.microphone as source:

                if not silent:
                    print("\n🎙️ Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            if not silent:
                print("🧠 Recognizing...")

            # Explicit English recognition
            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            text = text.strip()

            if not silent:

                print(
                    f"✅ Recognized: {text}"
                )

            return text

        except sr.WaitTimeoutError:

            return None

        except sr.UnknownValueError:

            if not silent:

                print(
                    "❌ I couldn't understand that."
                )

            return None

        except sr.RequestError as error:

            if not silent:

                print(
                    f"❌ Speech recognition service "
                    f"error: {error}"
                )

            return None

        except Exception as error:

            if not silent:

                print(
                    f"❌ Microphone error: {error}"
                )

            return None