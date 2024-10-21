import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSpinBox
from PyQt5.QtCore import Qt
from design import Ui_MainWindow

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Настройки")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.team1_edit = QLineEdit(self)
        self.team1_edit.setText(parent.team1_label.text())
        self.team2_edit = QLineEdit(self)
        self.team2_edit.setText(parent.team2_label.text())

        # Отдельные спинбоксы для минут и секунд
        self.minutes_edit = QSpinBox(self)
        self.minutes_edit.setRange(0, 59)  # Диапазон минут от 0 до 59
        self.minutes_edit.setValue(parent.initial_time // 60)  # Устанавливаем текущие минуты

        self.seconds_edit = QSpinBox(self)
        self.seconds_edit.setRange(0, 59)  # Диапазон секунд от 0 до 59
        self.seconds_edit.setValue(parent.initial_time % 60)  # Устанавливаем текущие секунды

        form_layout.addRow("Команда 1:", self.team1_edit)
        form_layout.addRow("Команда 2:", self.team2_edit)
        form_layout.addRow("Минуты:", self.minutes_edit)
        form_layout.addRow("Секунды:", self.seconds_edit)

        layout.addLayout(form_layout)

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        self.accept()  # Закрыть диалоговое окно и вернуть результат


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
        elif event.key() == Qt.Key_S:
            self.open_settings_dialog()  # Открываем окно настроек


    def open_settings_dialog(self):
        """Открываем диалог настроек."""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Обновляем названия команд
            self.team1_label.setText(dialog.team1_edit.text())
            self.team2_label.setText(dialog.team2_edit.text())

            # Обновляем время в секундах (минуты * 60 + секунды)
            self.initial_time = dialog.minutes_edit.value() * 60 + dialog.seconds_edit.value()
            self.reset_timer()  # Сбрасываем таймер после изменения времени


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
            self.state = "End"  # Меняем состояние на "Пауза"

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
            self.time_label.setText("||")  # Показать состояние "Пауза"
        elif self.state == "End":
            self.time_label.setText("Стоп!")  # Отображаем сообщение
        else:
            raise Exception("Error with state")


def application():
    """Запускаем приложение."""
    app = QApplication(sys.argv)
    window = Window()  # Создаем объект окна
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем главный цикл приложения


if __name__ == "__main__":
    application()  # Запускаем приложение
