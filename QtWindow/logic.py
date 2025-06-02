import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from QtWindow.design import Ui_MainWindow
from Tournament import Tournament
from dotenv import load_dotenv

load_dotenv()
api_url = os.getenv("API_URL")


class Window(QMainWindow, Ui_MainWindow):
    space_btn = pyqtSignal()
    esc_btn = pyqtSignal()
    prepare_end = pyqtSignal()
    update_all = pyqtSignal()

    def __init__(self):
        super().__init__()  # Инициализируем родительский класс
        self.setupUi(self)  # Настраиваем интерфейс
        self.connetctionStatus = 0
        if self.connetctionStatus == 0:
            self.tournament = Tournament(api_url=api_url)
            self.connetctionStatus = 1

        self.team_update_timer = QTimer()
        self.team_update_timer.start(1000)

        self.team_names = self.tournament.get_team_names()


        # Инициализация переменных
        self.initial_time = self.set_preparation_time(self.preparation_time)
        self.time_left = self.initial_time  # Оставшееся время
        self.state = "Idle"  # Начальное состояние таймера
        self.status = "Подготовка"

        while self.team_names == ["", ""]:
            print(self.team_names)
            self.get_team_names()
            self.apply_settings()
            self.update_time_label()
            if self.team_names != ["", ""]:
                print(self.team_names)

        # Устанавливаем время подготовки
        self.set_preparation_time(self.preparation_time)

        self.update_time_label()  # Обновляем метку времени

    def set_preparation_time(self, minutes):
        return minutes * 60

    def keyPressEvent(self, event):
        """Обрабатываем нажатия клавиш."""
        if event.key() == Qt.Key_Space:
            self.toggle_timer()
            self.space_btn.emit()
        elif event.key() in (Qt.Key_R, Qt.Key_K):
            self.restart_window()
        elif event.key() == Qt.Key_Escape:
            self.tournament.disconnect()
            self.connetctionStatus = 0
            self.esc_btn.emit()
            QApplication.quit()
        elif event.key() == Qt.Key_Left:
            if self.time_left + 5 >= self.initial_time:
                self.time_left = self.initial_time
            else:
                self.time_left += 5
            self.pause_timer()
            self.update_time_label()
        elif event.key() == Qt.Key_Right:
            if self.time_left - 5 <= 0:
                self.time_left = 0
            else:
                self.time_left -= 5
            self.pause_timer()
            self.update_time_label()
        elif event.key() == Qt.Key_U:
            self.update_window()

    def refery_handle(self):
        if self.status == "Подготовка" and self.state == "Ongoing":
            self.time_left = 0
        self.start_timer()

    def surrender(self):
        if self.status == "Подготовка":
            self.status = "Бой"
            self.state = "End"
            self.time_left = 0
        elif self.status == "Бой":
            self.time_left = 0
        self.update_time_label()
        FIFO_PATH = "/tmp/sound_pipe"
        try:
            with open(FIFO_PATH, "w") as pipe:
                pipe.write("stop")
            print("Сигнал на воспроизведение отправлен")
        except Exception as e:
            print(f"Ошибка отправки: {e}")

    def toggle_timer(self):
        """Запускаем или ставим на паузу таймер в зависимости от состояния."""
        if self.state == "Ongoing":
            self.pause_timer()  # Пауза
        else:
            self.start_timer()  # Запуск

    def start_timer(self):
        """Запускаем таймер."""
        self.state = "Ongoing"  # Меняем состояние на "Идет"
        self.timer.start()  # Запускаем таймер
        self.update_time_label()  # Обновляем метку времени

    def pause_timer(self):
        """Ставим таймер на паузу."""
        self.state = "Pause"  # Меняем состояние на "Пауза"
        self.timer.stop()  # Останавливаем таймер
        self.update_time_label()  # Обновляем метку времени

    def restart_window(self):
        """Перезапускаем программу."""
        print("Перезапуск программы...")
        self.tournament.disconnect()
        self.connetctionStatus = 0
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    def update_window(self):
        """ "Обновляет окно выставяя начальное положение"""
        self.state = "Idle"
        self.status = "Подготовка"
        self.initial_time = self.set_preparation_time(self.preparation_time)
        self.time_left = self.initial_time
        self.get_team_names()
        self.update_time_label()

    def update_timer(self):
        """Обновляем оставшееся время каждую секунду."""
        if self.time_left <= 0:
            if self.status == "Подготовка":
                self.initial_time = 3 * 60
                self.time_left = self.initial_time + 3
                self.status = "Бой"
                FIFO_PATH = "/tmp/sound_pipe"
                try:
                    with open(FIFO_PATH, "w") as pipe:
                        pipe.write("start")
                    print("Сигнал на воспроизведение отправлен")
                except Exception as e:
                    print(f"Ошибка отправки: {e}")
                self.prepare_end.emit()
            else:
                self.timer.stop()  # Останавливаем таймер, если время вышло
                self.state = "End"  # Меняем состояние на "End"
                self.update_time_label()  # Обновляем метку таймера
                self.update_window()  # Обновляем окно
        else:
            self.time_left -= 1  # Уменьшаем оставшееся время
            self.update_time_label()  # Обновляем метку времени

    def update_time_label(self):
        """Обновляем текст метки времени в зависимости от состояния."""
        if self.state == "Idle":
            self.time_label.setFont(QFont("Bebas Neue", 90))
            # Центрирование текста по горизонтали и вертикали
            self.time_label.setText(f'<div style="color:white; ">{self.status}</div>')

        elif self.state == "Ongoing":
            if self.time_left > self.initial_time:
                self.time_label.setFont(QFont("Bebas Neue", 125))
                # Центрирование текста по горизонтали и вертикали
                self.time_label.setText('<div style="color:white; ">Старт!</div>')
            else:
                self.time_label.setFont(QFont("Bebas Neue", 145))
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                # Центрирование текста по горизонтали и вертикали
                if self.time_left <= 10:
                    self.time_label.setText(
                        f'<div style="color:red;">{minutes:02d}:{seconds:02d}</div>'
                    )
                else:
                    self.time_label.setText(
                        f'<div style="color:white;">{minutes:02d}:{seconds:02d}</div>'
                    )

        elif self.state == "Pause":
            if self.time_left > self.initial_time:
                self.time_label.setFont(QFont("Bebas Neue", 125))
                # Центрирование текста по горизонтали и вертикали
                self.time_label.setText('<div style="color:white; ">Старт!</div>')
            else:
                self.time_label.setFont(QFont("Bebas Neue", 145))
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                # Центрирование текста по горизонтали и вертикали
                self.time_label.setText(
                    f'<div style="color:blue; ">{minutes:02d}:{seconds:02d}</div>'
                )

        elif self.state == "End":
            self.time_label.setFont(QFont("Bebas Neue", 145))
            # Центрирование текста по горизонтали и вертикали
            self.time_label.setText('<div style="color:white; ">Стоп!</div>')

        else:
            raise Exception("Error with state")

    def get_team_names(self):
        self.team_names = self.tournament.get_team_names()
        self.apply_settings()
        print(self.team_names)
