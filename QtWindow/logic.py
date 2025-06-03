import sys
import os
import time
import threading
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

    # Инициализация
    def __init__(self):
        super().__init__()
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
        self.time_left = self.initial_time
        self.state = "Idle"
        self.status = "Подготовка"

        self.team_names = ["Загрузка...", "Загрузка..."]
        self.apply_settings()
        self.update_time_label()

        threading.Thread(target=self.load_team_names, daemon=True).start()

        # Устанавливаем время подготовки
        self.set_preparation_time(self.preparation_time)

        self.update_time_label()

    # Загрузка названий команд с сервера
    def load_team_names(self):
        while self.state == "Idle":
            team_names = self.tournament.get_team_names()
            if team_names != self.team_names:
                self.team_names = team_names
                QTimer.singleShot(0, self.on_team_names_loaded)
                if self.state != "Idle":
                    break

            time.sleep(0.1)

    # Берёт данные о названиях команд с сервера
    def get_team_names(self):
        self.team_names = self.tournament.get_team_names()
        self.apply_settings()
        print(self.team_names)

    # Установка новых названий команд
    def on_team_names_loaded(self):
        self.apply_settings()
        self.update_time_label()
        print(f"Команды загружены: {self.team_names}")

    # Перевод минут в секунды
    def set_preparation_time(self, minutes):
        return minutes * 60

    # Обработчик ввода с клавиатуры
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:  # Остановить таймер
            self.toggle_timer()
            self.space_btn.emit()
        elif event.key() in (Qt.Key_R):  # Перезапуск программы
            self.restart_window()
        elif event.key() == Qt.Key_Escape:  # Завершение программы
            self.tournament.disconnect()
            self.connetctionStatus = 0
            self.esc_btn.emit()
            QApplication.quit()
        elif event.key() == Qt.Key_Left:  # Перемотка таймер на 5 секунд вперёд
            if self.time_left + 5 >= self.initial_time:
                self.time_left = self.initial_time
            else:
                self.time_left += 5
            self.pause_timer()
            self.update_time_label()
        elif event.key() == Qt.Key_Right:  # Перемотка таймер на 5 секунд назад
            if self.time_left - 5 <= 0:
                self.time_left = 0
            else:
                self.time_left -= 5
            self.pause_timer()
            self.update_time_label()
        elif event.key() == Qt.Key_S:  # Открывает диалоговое окно настроек
            self.show_settings_dialog()
        elif event.key() == Qt.Key_U:  # приводит систему в начальное положение
            self.update_window()

    # Обработчик сигнала с старта с кнопок судьи
    def refery_handle(self):
        if self.status == "Подготовка" and self.state == "Ongoing":
            self.time_left = 0
        self.start_timer()

    # Обработчик сигнала с кнопки сдаться
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

    # Переключения режима таймер
    def toggle_timer(self):
        if self.state == "Ongoing":
            self.pause_timer()
        else:
            self.start_timer()

    # Запуск таймера
    def start_timer(self):
        self.state = "Ongoing"
        self.timer.start()
        self.update_time_label()

    # Остановка таймера
    def pause_timer(self):
        self.state = "Pause"
        self.timer.stop()
        self.update_time_label()

    # Перезапуск программы
    def restart_window(self):
        print("Перезапуск программы...")
        self.tournament.disconnect()
        self.connetctionStatus = 0
        time.sleep(3)
        python = sys.executable
        os.execv(python, [python] + sys.argv)

    # Приводит систему к начальному состоянию
    def update_window(self):
        self.state = "Idle"
        self.status = "Подготовка"
        self.initial_time = self.set_preparation_time(self.preparation_time)
        self.time_left = self.initial_time
        threading.Thread(target=self.load_team_names, daemon=True).start()
        self.update_time_label()

    # Логика таймера
    def update_timer(self):
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
                self.timer.stop()
                self.state = "End"
                self.update_time_label()
                QTimer.singleShot(30000, self.update_window)
        else:
            self.time_left -= 1  # Уменьшаем оставшееся время
            self.update_time_label()

    # Обновление вывода таймера
    def update_time_label(self):
        if self.state == "Idle":
            self.time_label.setFont(QFont("Bebas Neue", 90))
            self.time_label.setText(f'<div style="color:white; ">{self.status}</div>')
        elif self.state == "Ongoing":
            if self.time_left > self.initial_time:
                self.time_label.setFont(QFont("Bebas Neue", 125))
                self.time_label.setText('<div style="color:white; ">Старт!</div>')
            else:
                self.time_label.setFont(QFont("Bebas Neue", 145))
                minutes = self.time_left // 60
                seconds = self.time_left % 60
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
                self.time_label.setText('<div style="color:white; ">Старт!</div>')
            else:
                self.time_label.setFont(QFont("Bebas Neue", 145))
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.time_label.setText(
                    f'<div style="color:blue; ">{minutes:02d}:{seconds:02d}</div>'
                )
        elif self.state == "End":
            self.time_label.setFont(QFont("Bebas Neue", 145))
            self.time_label.setText('<div style="color:white; ">Стоп!</div>')
        else:
            raise Exception("Error with state")
