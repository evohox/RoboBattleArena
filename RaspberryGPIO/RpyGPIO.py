import threading
import time
import os
import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, pyqtSignal
from rpi_ws281x import PixelStrip, Color
from dotenv import load_dotenv
from Tournament import Tournament
from RaspberryGPIO.LEDController import LEDController

load_dotenv()
api_url=os.getenv("API_URL")

class GPIOHandler(QObject):
    """Класс для обработки нажатия кнопок"""
    # Сигналы для внешних событий
    fight_started = pyqtSignal()
    fight_stopped = pyqtSignal()

    def __init__(self):
        """Инициализация работы системы."""
        self.tournament = Tournament(
            api_url=api_url
        )
        self.led = LEDController()

        self.lock = threading.Lock()
        self.threads = []

        # Состояния системы
        self.STATE_WAITING = 0
        self.STATE_READY = 1
        self.STATE_FIGHT = 2
        self.PREPARING = 3

        super().__init__()
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False

        # Настройка пинов для кнопок
        self.TEAM1_READY = 5
        self.TEAM1_STOP = 6
        self.TEAM2_READY = 19
        self.TEAM2_STOP = 13
        self.REFEREE_START = 26
        self.REFEREE_STOP = 16

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)

        self.buttons = [
            self.TEAM1_READY, self.TEAM1_STOP,
            self.TEAM2_READY, self.TEAM2_STOP,
            self.REFEREE_START, self.REFEREE_STOP
        ]

        for button in self.buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self._running = True

    def run_loop(self):
        """Обработка кнопок: реагирует только на нажатие с последующим отпусканием."""
        print("Starting!")

        previous_states = {button: GPIO.LOW for button in self.buttons}
        pressed_flags = {button: False for button in self.buttons}

        try:
            self.led.set_color(Color(0, 0, 0))
            threading.Thread(
                target=self.led.circle_color,
                args=(Color(0, 0, 255), Color(255, 0, 0), lambda: self.current_state == self.STATE_WAITING and self._running)
            ).start()


            while self._running:
                for button in self.buttons:
                    state = GPIO.input(button)

                    if state == GPIO.HIGH and previous_states[button] == GPIO.LOW:
                        pressed_flags[button] = True

                    elif state == GPIO.LOW and previous_states[button] == GPIO.HIGH and pressed_flags[button]:
                        pressed_flags[button] = False
                        t = threading.Thread(target=self.handle_button_press, args=(button,))
                        t.start()
                        self.threads.append(t)
                        print(self.current_state, self.team1_ready, self.team2_ready, button)

                    previous_states[button] = state

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.stop()
            print("Программа завершена.")



    def handle_button_press(self, button: int):
        """Обработка нажатия кнопки.
        Args:
            button (int): Номер нажатой кнопки.
        """
        print(button)
        if button == self.TEAM1_READY and self.current_state == self.PREPARING and not self.team1_ready:
            self.team1_ready = True
            self.led.fade_to_color(Color(0, 255, 0), team=1)  # Зеленый
            if self.team2_ready:
                self.current_state = self.STATE_READY
            FIFO_PATH = "/tmp/sound_pipe"
            try:
                with open(FIFO_PATH, "w") as pipe:
                    pipe.write("ready")
                print("Сигнал на воспроизведение отправлен")
            except Exception as e:
                print(f"Ошибка отправки: {e}")
            self.tournament.send_team1_ready()
        elif button == self.TEAM2_READY and self.current_state == self.PREPARING and not self.team2_ready:
            self.team2_ready = True
            self.led.fade_to_color(Color(0, 255, 0), team=2)  # Зеленый
            if self.team1_ready:
                self.current_state = self.STATE_READY
            FIFO_PATH = "/tmp/sound_pipe"
            try:
                with open(FIFO_PATH, "w") as pipe:
                    pipe.write("ready")
                print("Сигнал на воспроизведение отправлен")
            except Exception as e:
                print(f"Ошибка отправки: {e}")
            self.tournament.send_team2_ready()
        elif button == self.REFEREE_START and self.current_state != self.STATE_FIGHT:
            self.fight_started.emit()
            if self.current_state == self.STATE_WAITING:
                self.current_state = self.PREPARING
                self.tournament.send_preparing()
            else:
                self.current_state = self.STATE_FIGHT
                self.led.fade_to_color(Color(255, 0, 0), team=0)  # Красный
                self.tournament.send_fight_start()
        elif (button in [self.TEAM1_STOP, self.TEAM2_STOP, self.REFEREE_STOP]) and self.current_state != self.STATE_WAITING:
            self.fight_stopped.emit()
            self.reset_to_waiting()
            self.tournament.send_fight_end()

    def update_GPIO(self):
        self.STATE_WAITING = 0
        self.STATE_READY = 1
        self.STATE_FIGHT = 2
        self.PREPARING = 3
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False

    def end_prepare(self):
        """Окончание подготовки"""
        self.current_state = self.STATE_FIGHT
        self.led.set_color(Color(255, 0, 0))

    def reset_to_waiting(self):
        """Сброс в состояние ожидания"""
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        self.led.fade_to_color(Color(0, 0, 255))  # Синий

    def space_handler(self):
        """Обработка нажатия клавиши пробел на клавиатуре (если используется внещний таймер)"""
        if self.current_state == self.STATE_FIGHT:
            self.current_state = self.STATE_WAITING
            self.team1_ready = False
            self.team2_ready = False
            self.led.set_color(Color(0, 0, 255))  # Синий
        elif self.current_state == self.PREPARING:
            self.current_state = self.STATE_WAITING
            self.led.set_color(Color(0, 0, 255)) # Синий
        elif self.current_state == self.STATE_WAITING:
            self.current_state = self.PREPARING
            self.led.set_color(Color(0, 0, 255))

    def stop(self):
        """Остановка работы всей системы."""
        print("Stoping")
        for t in self.threads:
            t.join(timeout=0.1)
        self.tournament.disconnect()
        self.led.set_color(Color(0, 0, 0))
        self._running = False
        GPIO.cleanup()

def main():
    gpio_handler = GPIOHandler()
    gpio_handler.run_loop()

if __name__ == "__main__":
    main()
