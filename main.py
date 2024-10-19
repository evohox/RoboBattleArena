import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from PyQt5.QtCore import Qt
from design import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Инициализируем родительский класс
        self.setupUi(self)  # Настраиваем интерфейс

        # Инициализация переменных
        self.initial_time = 10 * 60  # 10 минут в секундах
        self.time_left = self.initial_time  # Оставшееся время
        self.state = "Idle"  # Начальное состояние таймера
        self.otschet = 4  # Обратный отсчет перед началом боя

        # Обновление метки времени
        self.update_time_label()

    def keyPressEvent(self, event):
        # Обрабатываем нажатие клавиш
        if event.key() == Qt.Key_Space:
            # Если состояние "Идет", ставим на паузу, иначе запускаем
            if self.state == "Ongoing":
                self.pause_timer()
            elif self.state == "Idle" or self.state == "Pause":
                self.start_timer()
        elif event.key() == Qt.Key_R or event.key() == Qt.Key_K:
            # Сброс таймера по нажатию R или K
            self.reset_timer()
        elif event.key() == Qt.Key_Escape:
            # Выход из приложения по нажатию Escape
            QApplication.quit()

    def start_timer(self):
        # Запускаем таймер, если он в состоянии паузы или "ожидания"
        if self.state == "Pause" or self.state == "Idle":
            self.state = "Ongoing"  # Меняем состояние на "Идет"
            self.otschet = 4  # Сбрасываем отсчет
            self.timer.start()  # Запускаем таймер
            self.update_time_label()  # Обновляем метку времени

    def pause_timer(self):
        # Ставим таймер на паузу, если он сейчас идет
        if self.state == "Ongoing" and not self.otschet:
            self.state = "Pause"  # Меняем состояние на "Пауза"
            self.timer.stop()  # Останавливаем таймер
            self.update_time_label()  # Обновляем метку времени

    def reset_timer(self):
        # Сбрасываем таймер
        self.state = "Idle"  # Меняем состояние на "Ожидание"
        self.timer.stop()  # Останавливаем таймер
        self.time_left = self.initial_time  # Возвращаем время к начальному
        self.update_time_label()  # Обновляем метку времени

    def update_timer(self):
        # Обновляем оставшееся время каждую секунду
        if self.time_left <= 1:
            self.timer.stop()  # Останавливаем таймер, если время вышло
            self.state = "Pause"  # Меняем состояние на "Пауза"
            self.time_label.setText("Время вышло!")  # Отображаем сообщение

        if self.otschet > 0:
            # Обрабатываем обратный отсчет
            self.otschet -= 1  # Уменьшаем отсчет на 1
            self.update_time_label()  # Обновляем метку времени
        else:
            # Уменьшаем оставшееся время
            self.time_left -= 1
            self.update_time_label()  # Обновляем метку времени

    def update_time_label(self):
        # Обновляем текст метки времени в зависимости от состояния
        if self.state == "Idle":
            self.time_label.setText("Arena")  # Показать название арены

        if self.state == "Ongoing":
            if self.otschet > 0:
                # Если идет обратный отсчет, показываем оставшееся время
                if self.otschet == 1:
                    self.time_label.setText(f"Бой!")  # Начало боя
                else:
                    self.time_label.setText(
                        f"{self.otschet - 1}"
                    )  # Осталось времени до боя
            else:
                # Показать оставшееся время в формате "минуты:секунды"
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

        if self.state == "Pause":
            self.time_label.setText("Пауза")  # Показать состояние "Пауза"


def application():
    # Запускаем приложение
    app = QApplication(sys.argv)
    window = Window()  # Создаем объект окна
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем главный цикл приложения


if __name__ == "__main__":
    application()  # Запускаем приложение
