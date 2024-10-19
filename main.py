import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        self.update_time_label()  # Обновляем метку времени

    def keyPressEvent(self, event):
        """Обрабатываем нажатия клавиш."""
        if event.key() == Qt.Key_Space:
            self.toggle_timer()  # Переключаем состояние таймера
        elif event.key() in (Qt.Key_R, Qt.Key_K):
            self.reset_timer()  # Сбрасываем таймер
        elif event.key() == Qt.Key_Escape:
            QApplication.quit()  # Выход из приложения

    def toggle_timer(self):
        """Запускаем или ставим на паузу таймер в зависимости от состояния."""
        if self.state == "Ongoing":
            self.pause_timer()  # Пауза
        else:
            self.start_timer()  # Запуск

    def start_timer(self):
        """Запускаем таймер."""
        if self.state in ("Idle", "Pause"):
            self.state = "Ongoing"  # Меняем состояние на "Идет"
            self.otschet = 4  # Сбрасываем отсчет
            self.timer.start()  # Запускаем таймер
            self.update_time_label()  # Обновляем метку времени

    def pause_timer(self):
        """Ставим таймер на паузу."""
        if self.state == "Ongoing" and self.otschet == 0:
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
        if self.time_left <= 1:
            self.timer.stop()  # Останавливаем таймер, если время вышло
            self.state = "Pause"  # Меняем состояние на "Пауза"
            self.time_label.setText("Время вышло!")  # Отображаем сообщение

        if self.otschet > 0:
            self.otschet -= 1  # Уменьшаем отсчет на 1
            self.update_time_label()  # Обновляем метку времени
        else:
            self.time_left -= 1  # Уменьшаем оставшееся время
            self.update_time_label()  # Обновляем метку времени

    def update_time_label(self):
        """Обновляем текст метки времени в зависимости от состояния."""
        if self.state == "Idle":
            self.time_label.setText("Arena")  # Показать название арены
        elif self.state == "Ongoing":
            if self.otschet > 0:
                self.time_label.setText(
                    "Бой!" if self.otschet == 1 else f"{self.otschet - 1}"
                )  # Осталось времени до боя
            else:
                minutes = self.time_left // 60
                seconds = self.time_left % 60
                self.time_label.setText(
                    f"{minutes:02d}:{seconds:02d}"
                )  # Форматирование времени
        elif self.state == "Pause":
            self.time_label.setText("Пауза")  # Показать состояние "Пауза"


def application():
    """Запускаем приложение."""
    app = QApplication(sys.argv)
    window = Window()  # Создаем объект окна
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем главный цикл приложения


if __name__ == "__main__":
    application()  # Запускаем приложение
