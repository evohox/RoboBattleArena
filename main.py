import sys
import threading
from PyQt5.QtWidgets import QApplication
from logic import Window
from RpyGPIO import GPIOHandler


def application():
    app = QApplication(sys.argv)
    window = Window()
    gpio_handler = GPIOHandler()

    # Запуск GPIO потока
    gpio_thread = threading.Thread(target=gpio_handler.run_loop, daemon=True)
    gpio_thread.start()

    # Подключение сигналов (предполагается, что это pyqtSignal)
    gpio_handler.fight_started.connect(window.refery_handle)
    gpio_handler.fight_stopped.connect(window.surrender)
    window.space_btn.connect(gpio_handler.space_handler)
    window.esc_btn.connect(gpio_handler.stop)
    window.prepare_end.connect(gpio_handler.end_prepare)

    window.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application exited with error: {e}")

if __name__ == "__main__":
    application()
