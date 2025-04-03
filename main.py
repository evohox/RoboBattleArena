import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from logic import Window


class AsyncRunner:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.timer = QTimer()
        self.timer.timeout.connect(self._run_async_tasks)
        self.timer.start(50)  # Проверяем asyncio задачи каждые 50мс

    def _run_async_tasks(self):
        """Обработка asyncio задач в основном цикле Qt"""
        self.loop.stop()
        self.loop.run_forever()


def application():
    app = QApplication(sys.argv)

    # Инициализация asyncio
    async_runner = AsyncRunner()
    asyncio.set_event_loop(async_runner.loop)

    window = Window()
    window.show()

    # Корректное завершение
    def shutdown():
        async_runner.loop.close()
        app.quit()

    window.destroyed.connect(shutdown)

    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        application()
    except KeyboardInterrupt:
        print("Приложение завершено")
        sys.exit(0)
