import sys
import math

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient
from PySide6.QtWidgets import QApplication, QWidget


class AssistantOrb(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(340, 340)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground)

        # Current assistant state
        self.state = "idle"

        # Animation variables
        self.angle = 0.0
        self.pulse = 0.0
        self.wave = 0.0

        # Approximately 60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    @Slot(str)
    def set_state(self, state):
        self.state = state.lower()
        print(f"ORB: {self.state.upper()}")
        self.update()

    def animate(self):
        if self.state == "idle":
            self.angle += 0.4
            self.pulse += 0.025

        elif self.state == "listening":
            self.angle += 1.0
            self.pulse += 0.06
            self.wave += 0.08

        elif self.state == "thinking":
            self.angle += 4.0
            self.pulse += 0.10

        elif self.state == "speaking":
            self.angle += 1.8
            self.pulse += 0.18
            self.wave += 0.12

        self.angle %= 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() // 2
        cy = self.height() // 2

        breathing = math.sin(self.pulse)

        # -----------------------
        # STATE-DEPENDENT SIZE
        # -----------------------

        if self.state == "idle":
            core_radius = 40 + breathing * 2
            glow_radius = 95 + breathing * 6

        elif self.state == "listening":
            core_radius = 43 + breathing * 4
            glow_radius = 105 + breathing * 10

        elif self.state == "thinking":
            core_radius = 41 + breathing * 3
            glow_radius = 100 + breathing * 7

        else:  # speaking
            core_radius = 45 + breathing * 7
            glow_radius = 110 + breathing * 12

        # -----------------------
        # OUTER GLOW
        # -----------------------

        glow = QRadialGradient(cx, cy, glow_radius)

        glow.setColorAt(0.0, QColor(130, 240, 255, 170))
        glow.setColorAt(0.4, QColor(40, 150, 255, 90))
        glow.setColorAt(1.0, QColor(0, 50, 160, 0))

        painter.setPen(Qt.NoPen)
        painter.setBrush(glow)

        painter.drawEllipse(
            int(cx - glow_radius),
            int(cy - glow_radius),
            int(glow_radius * 2),
            int(glow_radius * 2),
        )

        # -----------------------
        # LISTENING WAVES
        # -----------------------

        if self.state == "listening":
            for i in range(3):
                wave_position = (self.wave + i * 0.7) % 2.1

                radius = 82 + wave_position * 25

                alpha = int(max(0, 150 - wave_position * 65))

                wave_pen = QPen(QColor(100, 230, 255, alpha))

                wave_pen.setWidth(2)

                painter.setPen(wave_pen)
                painter.setBrush(Qt.NoBrush)

                painter.drawEllipse(
                    int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2)
                )

        # -----------------------
        # OUTER ROTATING RING
        # -----------------------

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(self.angle)

        outer_pen = QPen(QColor(80, 220, 255, 230))

        outer_pen.setWidth(4 if self.state == "thinking" else 3)

        painter.setPen(outer_pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawArc(-82, -82, 164, 164, 15 * 16, 105 * 16)

        painter.drawArc(-82, -82, 164, 164, 195 * 16, 105 * 16)

        painter.restore()

        # -----------------------
        # INNER ROTATING RING
        # -----------------------

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(-self.angle * 0.65)

        inner_pen = QPen(QColor(150, 245, 255, 170))

        inner_pen.setWidth(2)

        painter.setPen(inner_pen)

        painter.drawArc(-66, -66, 132, 132, 55 * 16, 85 * 16)

        painter.drawArc(-66, -66, 132, 132, 235 * 16, 85 * 16)

        painter.restore()

        # -----------------------
        # CORE
        # -----------------------

        core = QRadialGradient(cx, cy, core_radius)

        core.setColorAt(0.0, QColor(255, 255, 255, 255))

        core.setColorAt(0.22, QColor(150, 245, 255, 255))

        core.setColorAt(0.62, QColor(30, 145, 255, 235))

        core.setColorAt(1.0, QColor(0, 60, 190, 70))

        painter.setPen(Qt.NoPen)
        painter.setBrush(core)

        painter.drawEllipse(
            int(cx - core_radius),
            int(cy - core_radius),
            int(core_radius * 2),
            int(core_radius * 2),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    orb = AssistantOrb()
    orb.show()

    sys.exit(app.exec())
