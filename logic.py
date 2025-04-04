import sys
import asyncio
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QShortcut
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QCloseEvent, QKeySequence
from design import Ui_MainWindow
from settings import SettingsDialog
from RpyGPIO import GPIOHandler


class Window(QMainWindow, Ui_MainWindow):
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

        # Настройка шортката для закрытия
        self.close_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.close_shortcut.activated.connect(self.handle_close)

        # Устанавливаем время подготовки
        self.set_preparation_time(self.preparation_time)

        self.update_time_label()  # Обновляем метку времени

    async def run_loop(self):
        """Асинхронный цикл для интеграции с asyncio."""
        while True:
            await asyncio.sleep(0.001)  # Небольшая задержка, чтобы не нагружать CPU

    def set_preparation_time(self, minutes):
        return minutes * 60

    def keyPressEvent(self, event):
        """Обрабатываем нажатия клавиш."""
        if event.key() == Qt.Key_Space:
            self.toggle_timer()
        elif event.key() in (Qt.Key_R, Qt.Key_K):
            self.reset_timer()
        # elif event.key() == Qt.Key_Escape:
        #     print("Escape pressed. Closing.")
        #     self.close()
        elif event.key() == Qt.Key_S:
            self.open_settings_dialog()
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

    def handle_close(self):
        """Обработчик закрытия через Escape"""
        print("Close requested via Escape")
        self.close()  # Это вызовет closeEvent

    def closeEvent(self, event: QCloseEvent):
        """Вызывается при закрытии окна"""
        print("Close event triggered")

        # Получаем текущий event loop
        loop = None
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Запускаем корутину очистки
        if loop.is_running():
            # Если loop уже запущен, используем create_task
            asyncio.create_task(self.cleanup_and_exit())
        else:
            # Иначе запускаем loop
            loop.run_until_complete(self.cleanup_and_exit())

        event.accept()  # Подтверждаем закрытие

    async def cleanup_and_exit(self):
        """Корректное завершение программы"""
        print("Cleaning up...")
        try:
            await self.gpio_handler.stop()  # Ожидаем завершения GPIO
        except Exception as e:
            print(f"Ошибка при остановке GPIO: {e}")
        finally:
            # Гарантируем, что приложение закроется
            QApplication.quit()

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
        # if self.time_left <= 0:
        #     return
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
