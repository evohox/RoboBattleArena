import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from logic import Window
from RpyGPIO import GPIOHandler

class AsyncQtIntegration:
    def __init__(self, gpio_handler):
        self.gpio_handler = gpio_handler
        self.loop = asyncio.new_event_loop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_events)
        self.timer.start(10)  # 10ms интервал

    def process_events(self):
        # Обрабатываем asyncio события в Qt таймере
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def start(self):
        await self.gpio_handler.start()

def application():
    app = QApplication(sys.argv)
    window = Window()
    gpio_handler = GPIOHandler()

    # Подключение сигналов
    gpio_handler.fight_started.connect(window.start_timer)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Инициализация интеграции
    async_integration = AsyncQtIntegration(gpio_handler)
    asyncio.run_coroutine_threadsafe(async_integration.start(), async_integration.loop)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()
