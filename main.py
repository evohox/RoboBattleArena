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

    async def shutdown(self):
        """Корректное завершение всех задач и освобождение ресурсов"""
        # Отменяем все задачи
        tasks = [t for t in asyncio.all_tasks(self.loop) if not t.done()]
        for task in tasks:
            task.cancel()
        # Ожидаем завершения задач
        await asyncio.gather(*tasks, return_exceptions=True)
        # Останавливаем GPIO
        await self.gpio_handler.stop()
        # Останавливаем event loop
        self.loop.stop()

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

    # Обработка закрытия приложения
    def shutdown():
        """Корректное завершение приложения"""
        # Запускаем shutdown в потоке asyncio
        future = asyncio.run_coroutine_threadsafe(async_integration.shutdown(), async_integration.loop)
        try:
            future.result(timeout=5)  # Ждем максимум 5 секунд
        except Exception as e:
            print(f"Ошибка при завершении: {e}")
        finally:
            async_integration.loop.close()
            app.quit()

    # Привязываем shutdown к закрытию окна
    window.closeEvent = lambda event: shutdown()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Ошибка при выполнении приложения: {e}")
    finally:
        # Гарантируем остановку event loop
        async_integration.loop.call_soon_threadsafe(async_integration.loop.stop)

if __name__ == "__main__":
    application()
