import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from logic import Window
from RpyGPIO import GPIOHandler

class AsyncQtEventLoop:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_events)
        self.timer.start(10)  # 10ms интервал

    def process_events(self):
        """Обработка asyncio событий в Qt-таймере"""
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def run_tasks(self, *coros):
        """Запуск асинхронных задач"""
        tasks = [asyncio.create_task(coro) for coro in coros]
        await asyncio.gather(*tasks)

def main():
    app = QApplication(sys.argv)

    # Инициализация компонентов
    window = Window()
    gpio_handler = GPIOHandler()

    # Настройка сигналов
    gpio_handler.fight_started.connect(window.start_timer)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Инициализация asyncio event loop
    async_loop = AsyncQtEventLoop()
    asyncio.set_event_loop(async_loop.loop)

    # Запуск асинхронных задач
    async_loop.loop.run_until_complete(
        async_loop.run_tasks(
            gpio_handler.run_loop(),
            window.run_loop()
        )
    )

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
