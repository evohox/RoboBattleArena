import sys
from PyQt5.QtWidgets import QApplication
from logic import Window


def application():
    """Запускаем приложение."""
    app = QApplication(sys.argv)
    window = Window()  # Создаем объект окна
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # Запускаем главный цикл приложения


if __name__ == "__main__":
    application()  # Запускаем приложение
