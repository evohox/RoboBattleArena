import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from logic import Window
from RpyGPIO import GPIOHandler


async def application():
    """Запускаем приложение."""
    app = QApplication(sys.argv)

    # Создаем объект окна и обработчика GPIO
    window = Window()
    gpio_handler = GPIOHandler()

    # Подключаем сигналы GPIO к методам окна
    gpio_handler.fight_started.connect(window.start_timer)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Показываем окно
    window.show()

    # Запускаем асинхронный цикл для GPIOHandler
    async def run_gpio():
        await gpio_handler.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_gpio())

    # Запускаем главный цикл приложения
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()  # Запускаем приложение
