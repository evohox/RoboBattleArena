from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from design import Ui_MainWindow
from settings import SettingsDialog


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Инициализируем родительский класс
        self.setupUi(self)  # Настраиваем интерфейс

        # Инициализация переменных
        self.initial_time = 3 * 60  # 3 минут в секундах
        self.time_left = self.initial_time  # Оставшееся время
        self.state = "Idle"  # Начальное состояние таймера
        self.status = "Подготовка"

        self.update_time_label()  # Обновляем метку времени

    def keyPressEvent(self, event):
        """Обрабатываем нажатия клавиш."""
        if event.key() == Qt.Key_Space:
            self.toggle_timer()  # Переключаем состояние таймера
        elif event.key() in (Qt.Key_R, Qt.Key_K):
            self.reset_timer()  # Сбрасываем таймер
        elif event.key() == Qt.Key_Escape:
            QApplication.quit()  # Выход из приложения
        elif event.key() == Qt.Key_S:
            self.open_settings_dialog()  # Открываем окно настроек
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

    def open_settings_dialog(self):
        """Открываем диалог настроек."""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Обновляем названия команд
            self.team1_label.setText(dialog.team1_edit.text())
            self.team2_label.setText(dialog.team2_edit.text())

            # Обновляем время в секундах (минуты * 60 + секунды)
            self.initial_time = (
                dialog.minutes_edit.value() * 60 + dialog.seconds_edit.value()
            )
            self.reset_timer()  # Сбрасываем таймер после изменения времени

    def toggle_timer(self):
        """Запускаем или ставим на паузу таймер в зависимости от состояния."""
        if self.state == "Ongoing":
            self.pause_timer()  # Пауза
        else:
            self.start_timer()  # Запуск

    def start_timer(self):
        """Запускаем таймер."""
        if self.time_left <= 0:
            return
        self.state = "Ongoing"  # Меняем состояние на "Идет"
        self.timer.start()  # Запускаем таймер
        self.update_time_label()  # Обновляем метку времени

    def pause_timer(self):
        """Ставим таймер на паузу."""
        # if self.state == "Ongoing" or "Idle":
        self.state = "Pause"  # Меняем состояние на "Пауза"
        self.timer.stop()  # Останавливаем таймер
        self.update_time_label()  # Обновляем метку времени

    def reset_timer(self):
        """Сбрасываем таймер."""
        self.state = "Idle"  # Меняем состояние на "Ожидание"
        self.timer.stop()  # Останавливаем таймер
        self.time_left = self.initial_time  # Возвращаем время к начальному
        self.update_time_label()  # Обновляем метку времени

    def update_timer(self):
        """Обновляем оставшееся время каждую секунду."""
        if self.time_left <= 0:
            if self.status == "Подготовка":
                self.initial_time = 10 * 60
                self.time_left = self.initial_time + 3
                self.status = "Попытка"
                self.update_time_label()  # Обновляем метку времени
            else:
                self.timer.stop()  # Останавливаем таймер, если время вышло
                self.status = "Конец"
                self.state = "End"  # Меняем состояние на "End"
                self.update_time_label()  # Обновляем метку времени
        else:
            self.time_left -= 1  # Уменьшаем оставшееся время
            self.update_time_label()  # Обновляем метку времени

    def update_time_label(self):
        """Обновляем текст метки времени в зависимости от состояния."""
        if self.state == "Idle":
            self.time_label.setFont(QFont("Bebas Neue", 140))
            # Центрирование текста по горизонтали и вертикали
            self.time_label.setText('<div style="color:white; ">Arena</div>')

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