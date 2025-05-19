import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from logic import Window
from RpyGPIO import GPIOHandler
import threading


def application():
    app = QApplication(sys.argv)
    window = Window()
    gpio_handler = GPIOHandler()
    gpio_thread = threading.Thread(target=gpio_handler.run_loop, daemon=True).start()
    
    # Подключение сигналов
    gpio_handler.fight_started.connect(window.refery_handle)
    gpio_handler.fight_stopped.connect(window.pause_timer)
    window.space_btn.connect(gpio_handler.space_handler)
    window.esc_btn.connect(gpio_handler.stop)

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    application()
