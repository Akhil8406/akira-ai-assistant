import os
import time

import numpy as np
import sounddevice as sd
from openwakeword.model import Model


class WakeWordDetector:
    def __init__(
        self,
        model_path=None,
        threshold=0.5,
        sample_rate=16000,
        block_size=1280,
    ):
        if model_path is None:
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )

            model_path = os.path.join(
                project_root,
                "assets",
                "wakeword",
                "hey_akira.onnx",
            )

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Wake-word model not found:\n{model_path}")

        self.model_path = model_path
        self.threshold = threshold
        self.sample_rate = sample_rate
        self.block_size = block_size

        print("Loading AKIRA wake-word model...")

        self.model = Model(
            wakeword_models=[self.model_path],
            inference_framework="onnx",
        )

        print("AKIRA wake-word model loaded.")

    def wait_for_wake_word(self):
        """
        Blocks until 'Hey Akira' is detected.
        """

        print("\n💤 AKIRA sleeping...")
        print("🎤 Waiting for 'Hey Akira'...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.block_size,
        ) as stream:
            while True:
                audio, overflowed = stream.read(self.block_size)

                if overflowed:
                    continue

                audio = np.squeeze(audio)

                predictions = self.model.predict(audio)

                for model_name, score in predictions.items():
                    if score >= self.threshold:
                        print(f"🔥 Wake word detected! ({model_name}: {score:.2f})")

                        # Small cooldown so the wake phrase itself
                        # isn't captured as part of the command.
                        time.sleep(0.35)

                        return True
