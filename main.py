import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop, asyncSlot  # Необходимо установить: pip install qasync
from logic import Window
from RpyGPIO import GPIOHandler


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = Window()
        self.gpio_handler = GPIOHandler()

        # Подключаем сигналы
        self.gpio_handler.fight_started.connect(self.window.start_timer)
        self.gpio_handler.fight_stopped.connect(self.window.pause_timer)

        # Настраиваем обработчик закрытия окна
        self.window.closeEvent = self.on_close

    async def run_gpio(self):
        """Запуск GPIO обработчика"""
        try:
            await self.gpio_handler.run_loop()
        except asyncio.CancelledError:
            await self.gpio_handler.stop()

    @asyncSlot()
    async def on_close(self, event):
        """Обработчик закрытия окна"""
        await self.gpio_handler.stop()
        event.accept()

    def run(self):
        """Запуск приложения"""
        self.window.show()

        # Создаем и запускаем задачу для GPIO
        loop = asyncio.get_event_loop()
        gpio_task = loop.create_task(self.run_gpio())

        # Запускаем Qt-приложение
        exit_code = self.app.exec_()

        # Останавливаем задачи при завершении
        gpio_task.cancel()
        loop.run_until_complete(gpio_task)

        sys.exit(exit_code)


if __name__ == "__main__":
    # Настраиваем интеграцию asyncio с Qt
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    # Запускаем наше приложение
    main_app = Application()

    with loop:
        loop.run_until_complete(main_app.run())
