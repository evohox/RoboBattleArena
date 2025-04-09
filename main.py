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
        self.timer.start(1)  # Период обработки событий asyncio

    def process_events(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    async def start(self):
        await asyncio.gather(
            self.gpio_handler.run_loop(),
            self.window.run_loop()
        )

def application():
    app = QApplication(sys.argv)
    window = Window()
    gpio_handler = GPIOHandler()

    # Подключение сигналов
    gpio_handler.fight_started.connect(window.refery_handle)
    gpio_handler.fight_stopped.connect(window.pause_timer)

    # Инициализация интеграции
    async_integration = AsyncQtIntegration(gpio_handler, window)
    asyncio.run_coroutine_threadsafe(
        async_integration.start(), async_integration.loop
    )

    window.show()

    def shutdown():
        """Корректное завершение приложения с остановкой asyncio-задач."""
        def _shutdown_in_loop():
            try:
                # Отменяем все задачи
                tasks = asyncio.all_tasks(async_integration.loop)
                for task in tasks:
                    task.cancel()

                # Собираем отмененные задачи без timeout
                async def _gather_cancelled():
                    try:
                        await asyncio.gather(*tasks, return_exceptions=True)
                    except:
                        pass

                # Запускаем сбор отмененных задач
                future = asyncio.run_coroutine_threadsafe(
                    _gather_cancelled(), async_integration.loop
                )
                # Убираем timeout или увеличиваем его
                future.result()  # Убрали timeout=2

            except Exception as e:
                print(f"Ошибка при завершении: {e}")
            finally:
                async_integration.loop.call_soon_threadsafe(async_integration.loop.stop)
                app.quit()

        async_integration.loop.call_soon_threadsafe(_shutdown_in_loop)

    window.closeEvent = lambda event: shutdown()

    try:
        sys.exit(app.exec_())
    finally:
        async_integration.loop.call_soon_threadsafe(async_integration.loop.stop)

if __name__ == "__main__":
    application()
