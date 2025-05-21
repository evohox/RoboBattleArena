import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5.QtCore import Qt, QCoreApplication, QProcess, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound
from design import Ui_MainWindow
from RpyGPIO import GPIOHandler
import subprocess
import pygame

class Window(QMainWindow, Ui_MainWindow):
    space_btn = pyqtSignal()
    esc_btn = pyqtSignal()

    def __init__(self):
        super().__init__()  # Инициализируем родительский класс
        self.setupUi(self)  # Настраиваем интерфейс

        # Инициализация GPIOHandler
        self.gpio_handler = GPIOHandler()

        # Инициализация переменных
        self.initial_time = self.set_preparation_time(self.preparation_time)
        self.time_left = self.initial_time  # Оставшееся время
        self.state = "Idle"  # Начальное состояние таймера
        self.status = "Подготовка"
        # self.sound = QSound("fixed_sound.wav")


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
            self.reset_timer()
        elif event.key() == Qt.Key_Escape:
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

    def reset_timer(self):
        """Сбрасываем таймер."""
        QCoreApplication.quit()
        QProcess.startDetached(sys.executable, sys.argv)


    def update_timer(self):
        """Обновляем оставшееся время каждую секунду."""
        if self.time_left <= 0:
            if self.status == "Подготовка":
                self.initial_time = 3 * 60
                self.time_left = self.initial_time + 3
                self.status = "Бой"
                self.update_time_label()  # Обновляем метку времени
                # pygame.mixer.init()
                # pygame.mixer.music.load('/home/admin/project/RoboBattleArena/fixed_sound.wav')
                # pygame.mixer.music.play()
                subprocess.run("sudo aplay /home/admin/project/RoboBattleArena/fixed_sound.wav", shell=True)
            else:
                self.timer.stop()  # Останавливаем таймер, если время вышло
                self.state = "End"  # Меняем состояние на "End"
                self.update_time_label()  # Обновляем метку времени
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
