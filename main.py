import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5.QtCore import Qt
from design import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Инициализация переменных
        self.initial_time = 10 * 60  # 10 минут в секундах
        self.time_left = self.initial_time
        self.state = "Idle"
        self.otschet = 4

        # Обновление метки времени
        self.update_time_label()

    def keyPressEvent(self, event):
        # Обрабатываем нажатие клавиш
        if event.key() == Qt.Key_Space:
            if self.state == "Ongoing":
                self.pause_timer()
            elif self.state == "Idle" or self.state == "Pause":
                self.start_timer()
        elif event.key() == Qt.Key_R or event.key() == Qt.Key_K:
            self.reset_timer()
        elif event.key() == Qt.Key_Escape:
            QApplication.quit()

    def start_timer(self):
        if self.state == "Pause" or self.state == "Idle":
            self.state = "Ongoing"
            self.otschet = 4
            self.timer.start()
            self.update_time_label()

    def pause_timer(self):
        if self.state == "Ongoing" and not self.otschet:
            self.state = "Pause"
            self.timer.stop()
            self.update_time_label()

    def reset_timer(self):
        self.state = "Idle"
        self.timer.stop()
        self.time_left = self.initial_time
        self.update_time_label()

    def update_timer(self):
        if self.time_left <= 1:
            self.timer.stop()
            self.state = "Pause"
            self.time_label.setText("Время вышло!")

        if self.otschet > 0:
            self.otschet -= 1
            self.update_time_label()
        else:
            self.time_left -= 1
            self.update_time_label()

    def update_time_label(self):
        if self.state == "Idle":
            self.time_label.setText("Arena")

        if self.state == "Ongoing":
            if self.otschet > 0:
                if self.otschet == 1:
                    self.time_label.setText(f"Бой!")
                else:
                    self.time_label.setText(f"{self.otschet - 1}")
            else:
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

        if self.state == "Pause":
            self.time_label.setText("Пауза")


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
