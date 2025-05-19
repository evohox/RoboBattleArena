import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, pyqtSignal
from rpi_ws281x import PixelStrip, Color
import threading
import time
from dotenv import load_dotenv
import os
from Tournament import Tournament

load_dotenv()
login=os.getenv("login")
password=os.getenv("password")
api_url=os.getenv("api_url")
fight_id = os.getenv("fight_id")

class GPIOHandler(QObject):
    # Сигналы для внешних событий
    fight_started = pyqtSignal()
    fight_stopped = pyqtSignal()

    def __init__(self):
        # self.tournament = Tournament(id=fight_id, login=login, password=password, api_url=api_url)
        self.lock = threading.Lock()
        # Настройки по умолчанию
        self.LED_COUNT = 180
        self.LED_PIN = 18
        self.LED_FREQ_HZ = 800000
        self.LED_DMA = 10
        self.LED_BRIGHTNESS = 255
        self.LED_INVERT = False
        self.LED_CHANNEL = 0

        # Состояния системы
        self.STATE_WAITING = 0
        self.STATE_READY = 1
        self.STATE_FIGHT = 2
        self.PREPARING = 3


        super().__init__()
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        self.team1_ready_event = threading.Event()
        self.team2_ready_event = threading.Event()
        self.team1_stop_event = threading.Event()
        self.team2_stop_event = threading.Event()
        self.referee_start_event = threading.Event()
        self.referee_stop_event = threading.Event()


        # Настройка пинов для кнопок
        self.TEAM1_READY = 5
        self.TEAM1_STOP = 6
        self.TEAM2_READY = 19
        self.TEAM2_STOP = 13
        self.REFEREE_START = 26
        self.REFEREE_STOP = 16

        # Настройка светодиодной ленты
        self.strip = PixelStrip(
            self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,
            self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL
        )
        self.strip.begin()

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)

        self.buttons = [
            self.TEAM1_READY, self.TEAM1_STOP,
            self.TEAM2_READY, self.TEAM2_STOP,
            self.REFEREE_START, self.REFEREE_STOP
        ]

        for button in self.buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self._running = False
        self._task = None

    def run_loop(self):
        """Основной цикл обработки кнопок"""
        print("Starting!")
        try:
        # Инициализация - синий цвет
            self.set_color(Color(0, 0, 255))

            while True:
                # Проверка всех кнопок
                for button in self.buttons:
                    if GPIO.input(button) == GPIO.HIGH:
                        # self.handle_button_press(button)
                        threading.Thread(target=self.handle_button_press, args=(button, )).start()
                        time.sleep(0.1)  # Задержка для антидребезга
                        print(self.current_state, self.team1_ready, self.team2_ready, button)


                time.sleep(0.05)

        except KeyboardInterrupt:
            self.set_color(Color(0, 0, 0))  # Выключить все светодиоды
            GPIO.cleanup()
            print("Программа завершена.")

    def handle_button_press(self, button):
        """Обработка нажатия кнопки"""
        print(button)
        if button == self.TEAM1_READY and self.current_state == self.PREPARING and not self.team1_ready:
            self.team1_ready = True
            self.fade_to_color(Color(0, 255, 0), team=1)  # Зеленый
            if self.team2_ready:
                self.current_state = self.STATE_READY
            # result = self.tournament.set_ready("565", "first_ready", "https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
            # result = self.tournament.reload_page("https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
        elif button == self.TEAM2_READY and self.current_state == self.PREPARING and not self.team2_ready:
            self.team2_ready = True
            self.fade_to_color(Color(0, 255, 0), team=2)  # Зеленый
            if self.team1_ready:
                self.current_state = self.STATE_READY
            # result = self.tournament.set_ready("565", "second_ready", "https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
            # result = self.tournament.reload_page("https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
        elif button == self.REFEREE_START and self.current_state != self.STATE_FIGHT:
            if self.current_state == self.STATE_WAITING:
                self.current_state = self.PREPARING
                self.fight_started.emit()
            else:
                self.current_state = self.STATE_FIGHT
                self.fight_started.emit()
                self.fade_to_color(Color(255, 0, 0), team=0, duration=2)  # Красный
            # result = self.tournament.setfight("565", "2", "https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
            # result = self.tournament.reload_page("https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
        elif (button in [self.TEAM1_STOP, self.TEAM2_STOP, self.REFEREE_STOP]) and self.current_state != self.STATE_WAITING:
            self.fight_stopped.emit()
            self.reset_to_waiting()
            # result = self.tournament.setfight("565", "3", "https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)
            # result = self.tournament.reload_page("https://grmvzdlx-3008.euw.devtunnels.ms")
            # print(result)


    def space_handler(self):
        if self.current_state == self.STATE_FIGHT:
            self.current_state = self.STATE_WAITING
            self.team1_ready = False
            self.team2_ready = False
            self.fade_to_color(Color(0, 0, 255))  # Синий
        elif self.current_state == self.STATE_WAITING:
            self.current_state = self.STATE_FIGHT
            self.fade_to_color(Color(255, 0, 0), team=0, duration=2)


    def set_color(self, color, team=0):
        """Установка цвета всей ленты"""
        if team == 1:
                for i in range(90, self.strip.numPixels()):
                    self.strip.setPixelColor(i, color)
        elif team == 2:
            for i in range(self.strip.numPixels()-90):
                self.strip.setPixelColor(i, color)
        else:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
        self.strip.show()
        # if duration > 0:
        #     time.sleep(duration)

    def fade_to_color(self, target_color, team=0, duration=0.5):
        """Плавный переход к указанному цвету"""
        steps = 100
        delay = duration / steps

        if team==2:
            current_color = self.strip.getPixelColor(0)
        else:
            current_color = self.strip.getPixelColor(91)
        current_r = (current_color >> 16) & 0xff
        current_g = (current_color >> 8) & 0xff
        current_b = current_color & 0xff

        target_r = (target_color >> 16) & 0xff
        target_g = (target_color >> 8) & 0xff
        target_b = target_color & 0xff

        with self.lock:
            for step in range(steps):
                r = int(current_r + (target_r - current_r) * (step / steps))
                g = int(current_g + (target_g - current_g) * (step / steps))
                b = int(current_b + (target_b - current_b) * (step / steps))

                self.set_color(Color(r, g, b), team=team)
                time.sleep(delay)

    def blink(self, target_color, team=0, duration=2.0):
        """Мигание цветом"""

        current_color = self.strip.getPixelColor(0)

        self.fade_to_color(target_color, team=team, duration=duration/2)
        self.fade_to_color(current_color, team=team, duration=duration/2)

    def reset_to_waiting(self):
        """Сброс в состояние ожидания"""
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        self.fade_to_color(Color(0, 0, 255))  # Синий

    def stop(self):
        print("Stoping")
        self.set_color(Color(0, 0, 0))
        self._running = False
        GPIO.cleanup()

def main():
	gpio_handler = GPIOHandler()
	gpio_handler.run_loop()

if __name__ == "__main__":
  main()
