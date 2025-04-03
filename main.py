import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from logic import Window
from qasync import QEventLoop, asyncSlot


def application():
    """Запускаем приложение с интеграцией asyncio."""
    app = QApplication(sys.argv)

    # Настраиваем asyncio-интеграцию
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = Window()
    window.show()

    with loop:
        try:
            loop.run_forever()
        finally:
            loop.close()


if __name__ == "__main__":
    # Для корректного завершения приложения
    try:
        application()
    except KeyboardInterrupt:
        print("Приложение завершено")
        sys.exit(0)
