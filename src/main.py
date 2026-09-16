import sys
import threading
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication

from src.ui.orb import AssistantOrb
from src.core.assistant import Assistant
from src.voice.wakeword import WakeWordDetector


# ======================================================
# VOICE ASSISTANT
# ======================================================


class AssistantWorker(QThread):
    state_changed = Signal(str)
    show_orb = Signal()
    hide_orb = Signal()

    def __init__(self, assistant, voice_lock):
        super().__init__()

        self.assistant = assistant
        self.voice_lock = voice_lock

        # Custom local "Hey Akira" model
        self.wake_detector = WakeWordDetector(threshold=0.50)

    def run(self):
        print("\n💤 AKIRA is running silently in the background.")
        print("🎙️ Say 'Hey Akira' to wake me.")

        while True:
            self.state_changed.emit("idle")
            self.hide_orb.emit()

            try:
                # ==================================================
                # WAIT FOR CUSTOM WAKE WORD
                # ==================================================

                print("\n💤 Waiting for Hey Akira...")

                with self.voice_lock:
                    detected = self.wake_detector.wait_for_wake_word()

                if not detected:
                    continue

                # ==================================================
                # AKIRA ACTIVATED
                # ==================================================

                print("\n⚡ AKIRA ACTIVATED")

                self.show_orb.emit()

                # ==================================================
                # ACKNOWLEDGE
                # ==================================================

                self.state_changed.emit("speaking")

                with self.voice_lock:
                    self.assistant.speaker.speak("Yes?")

                # ==================================================
                # IMPORTANT:
                # Give Windows time to release audio devices.
                #
                # openWakeWord uses sounddevice.
                # listener.py then opens the microphone separately.
                # ==================================================

                time.sleep(1.0)

                # ==================================================
                # COMMAND LISTENER
                # ==================================================

                self.state_changed.emit("listening")

                print("\n🎙️ COMMAND LISTENER STARTING...")

                command = None

                try:
                    with self.voice_lock:
                        command = self.assistant.listener.listen(silent=False)

                except Exception as error:
                    print(f"❌ Command microphone error: {error}")

                    command = None

                # ==================================================
                # NOTHING UNDERSTOOD
                # ==================================================

                if command is None:
                    print("❌ No command was understood.")

                    self.state_changed.emit("idle")

                    self.hide_orb.emit()

                    time.sleep(0.5)

                    continue

                command = command.strip()

                if not command:
                    print("❌ Empty command received.")

                    self.state_changed.emit("idle")

                    self.hide_orb.emit()

                    time.sleep(0.5)

                    continue

                # ==================================================
                # COMMAND RECEIVED
                # ==================================================

                print(f"\n👤 COMMAND: {command}")

                # ==================================================
                # THINKING
                # ==================================================

                self.state_changed.emit("thinking")

                try:
                    response = self.assistant.process_command(command)

                except Exception as error:
                    print(f"❌ Command processing error: {error}")

                    response = (
                        "Sorry, something went wrong while processing that command."
                    )

                # ==================================================
                # SPEAK RESPONSE
                # ==================================================

                if response:
                    print(f"🤖 AKIRA: {response}")

                    self.state_changed.emit("speaking")

                    try:
                        with self.voice_lock:
                            self.assistant.speaker.speak(response)

                    except Exception as error:
                        print(f"❌ Speech error: {error}")

                # ==================================================
                # RETURN TO SLEEP
                # ==================================================

                self.state_changed.emit("idle")

                self.hide_orb.emit()

                print("\n💤 Returning to wake-word mode...")

                # Prevent AKIRA's own speech from
                # immediately retriggering the wake word.
                time.sleep(0.7)

            except Exception as error:
                print(f"\n❌ Voice assistant error: {error}")

                self.state_changed.emit("idle")

                self.hide_orb.emit()

                time.sleep(1)


# ======================================================
# EMAIL MONITOR
# ======================================================


class EmailMonitor(QThread):
    important_email = Signal(str)

    def __init__(self, assistant):
        super().__init__()

        self.assistant = assistant

        # Check Gmail every 2 minutes
        self.check_interval = 120

        self.seen_ids = set()

        self.first_check = True

    def run(self):
        print("\n📧 Email monitor started.")

        while True:
            try:
                print("\n📡 AKIRA scanning Gmail...")

                emails = self.assistant.gmail.get_unread_emails(20)

                print(f"📬 Found {len(emails)} recent unread email(s).")

                # ==================================================
                # FIRST CHECK
                # ==================================================

                if self.first_check:
                    for email in emails:
                        self.seen_ids.add(email["id"])

                    self.first_check = False

                    print("📧 Email monitor ready.")

                    time.sleep(self.check_interval)

                    continue

                # ==================================================
                # NEW EMAIL CHECK
                # ==================================================

                for email in reversed(emails):
                    message_id = email["id"]

                    if message_id in self.seen_ids:
                        continue

                    self.seen_ids.add(message_id)

                    print("\n📨 New email detected:")

                    print(email["subject"])

                    # ==============================================
                    # CLASSIFY EMAIL
                    # ==============================================

                    try:
                        important = self.assistant.classify_email(email)

                    except Exception as error:
                        print(f"❌ Email classification error: {error}")

                        continue

                    if not important:
                        print("🔕 Email ignored.")

                        continue

                    print("🚨 Important email detected.")

                    # ==============================================
                    # CREATE ALERT
                    # ==============================================

                    try:
                        alert = self.assistant.create_email_alert(email)

                        if alert:
                            self.important_email.emit(alert)

                    except Exception as error:
                        print(f"❌ Email alert error: {error}")

            except Exception as error:
                print(f"❌ Email monitor error: {error}")

            # ======================================================
            # WAIT BEFORE NEXT EMAIL CHECK
            # ======================================================

            time.sleep(self.check_interval)


# ======================================================
# MAIN
# ======================================================


def main():
    # ==================================================
    # QT APPLICATION
    # ==================================================

    app = QApplication(sys.argv)

    # ==================================================
    # CREATE AKIRA
    # ==================================================

    print("\n⚡ Starting AKIRA...")

    assistant = Assistant()

    # ==================================================
    # AUDIO LOCK
    # ==================================================
    #
    # Wake-word detection, speech recognition and
    # AKIRA's voice should never use the audio system
    # simultaneously.
    #
    # ==================================================

    voice_lock = threading.Lock()

    # ==================================================
    # ORB
    # ==================================================

    orb = AssistantOrb()

    screen = app.primaryScreen().availableGeometry()

    x = screen.center().x() - orb.width() // 2

    y = screen.center().y() - orb.height() // 2

    orb.move(x, y)

    orb.hide()

    # ==================================================
    # VOICE WORKER
    # ==================================================

    worker = AssistantWorker(assistant, voice_lock)

    worker.state_changed.connect(orb.set_state)

    worker.show_orb.connect(orb.show)

    worker.hide_orb.connect(orb.hide)

    # ==================================================
    # EMAIL MONITOR
    # ==================================================

    email_monitor = EmailMonitor(assistant)

    # ==================================================
    # EMAIL VOICE ANNOUNCEMENT
    # ==================================================

    def announce_email(message):
        print(f"\n🔊 AKIRA EMAIL ALERT: {message}")

        orb.show()

        orb.set_state("speaking")

        try:
            with voice_lock:
                assistant.speaker.speak(message)

        except Exception as error:
            print(f"❌ Email speech error: {error}")

        orb.set_state("idle")

        orb.hide()

    email_monitor.important_email.connect(announce_email)

    # ==================================================
    # START EVERYTHING
    # ==================================================

    worker.start()

    email_monitor.start()

    # ==================================================
    # KEEP REFERENCES ALIVE
    # ==================================================

    app.worker = worker
    app.email_monitor = email_monitor
    app.assistant = assistant
    app.voice_lock = voice_lock
    app.orb = orb

    # ==================================================
    # QT LOOP
    # ==================================================

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
