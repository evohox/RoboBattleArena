import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from logic import Window
from RpyGPIO import GPIOHandler


async def run_gpio(gpio_handler):
    """Асинхронная задача для работы GPIO"""
    await gpio_handler.run_loop()


def application():
    """Запускаем приложение."""
    app = QApplication(sys.argv)

    # Создаем объект окна и обработчика GPIO
    window = Window()
    gpio_handler = GPIOHandler()

    # Подключаем сигналы GPIO к методам окна
    gpio_handler.fight_started.connect(window.start_timer)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Создаем и настраиваем event loop
    loop = asyncio.get_event_loop()

    # Создаем задачу для GPIO
    gpio_task = loop.create_task(run_gpio(gpio_handler))

    # Показываем окно
    window.show()

    # Запускаем главный цикл приложения
    exit_code = app.exec_()

    # Останавливаем GPIO при завершении
    gpio_task.cancel()
    try:
        loop.run_until_complete(gpio_task)
    except asyncio.CancelledError:
        pass

    sys.exit(exit_code)


if __name__ == "__main__":
    application()
