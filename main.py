import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from logic import Window
from RpyGPIO import GPIOHandler

class AsyncQtIntegration:
    def __init__(self, gpio_handler, window):
        self.gpio_handler = gpio_handler
        self.window = window
        self.loop = asyncio.new_event_loop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_events)
        self.timer.start(1)

    def process_events(self):
        # Обрабатываем asyncio события в Qt таймере
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def start(self):
        # Запускаем обработчик GPIO и окно параллельно
        await asyncio.gather(
            self.gpio_handler.run_loop(),
            self.window.run_loop()
        )

def application():
    app = QApplication(sys.argv)
    window = Window()
    gpio_handler = GPIOHandler()

    # Подключение сигналов
    gpio_handler.fight_started.connect(window.start_timer)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Инициализация интеграции
    async_integration = AsyncQtIntegration(gpio_handler, window)
    asyncio.run_coroutine_threadsafe(async_integration.start(), async_integration.loop)

    window.show()

    try:
        sys.exit(app.exec_())
    finally:
        # Корректное завершение event loop при выходе
        async_integration.loop.call_soon_threadsafe(async_integration.loop.stop)

if __name__ == "__main__":
    application()
