import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color
from playsound import playsound
from PyQt5.QtCore import QObject, pyqtSignal
# import pyglet
# sound = pyglet.media.load("//home//admin//project//buttons//start.mp3")
# sound.play()


class GPIOHandler(QObject):
    fight_started = pyqtSignal()  # Сигнал без параметров
    fight_stopped = pyqtSignal()
    def __init__(self):
        super().__init__()
        # Настройки светодиодной ленты
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
        self.current_state = self.STATE_WAITING

        # Настройка пинов для кнопок
        self.TEAM1_READY = 6
        self.TEAM1_STOP = 5
        self.TEAM2_READY = 13
        self.TEAM2_STOP = 16
        self.REFEREE_START = 19
        self.REFEREE_STOP = 26

        # Флаги готовности команд
        self.team1_ready = False
        self.team2_ready = False


    def setup_lef_strip(self):
        # Инициализация светодиодной ленты
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        self.strip.begin()


    def setup_GPIO(self):
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        buttons = [self.TEAM1_READY, self.TEAM1_STOP, self.TEAM2_READY, self.TEAM2_STOP, self.REFEREE_START, self.REFEREE_STOP]
        for button in buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_color(self, color, duration=0):
        """Установка цвета всей ленты"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        if duration > 0:
            time.sleep(duration)

    def fade_to_color(self, target_color, duration=1.0):
        """Плавный переход к указанному цвету"""
        steps = 100
        delay = duration / steps

        current_color = self.strip.getPixelColor(0)
        current_r = (current_color >> 16) & 0xff
        current_g = (current_color >> 8) & 0xff
        current_b = current_color & 0xff

        target_r = (target_color >> 16) & 0xff
        target_g = (target_color >> 8) & 0xff
        target_b = target_color & 0xff

        for step in range(steps):
            r = int(current_r + (target_r - current_r) * (step / steps))
            g = int(current_g + (target_g - current_g) * (step / steps))
            b = int(current_b + (target_b - current_b) * (step / steps))

            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(r, g, b))
            self.strip.show()
            time.sleep(delay)

    def reset_to_waiting(self):
        """Сброс в состояние ожидания"""
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        self.fade_to_color(Color(0, 0, 255))  # Синий
        self.fight_stopped.emit()

    def handle_button_press(self, button):
        """Обработка нажатия кнопок"""

        if button == self.TEAM1_READY and self.current_state == self.STATE_WAITING:
            team1_ready = True
            self.set_color(Color(0, 255, 0), 0)  # Зеленый на 2 секунды
            if self.team2_ready:
                self.current_state = self.STATE_READY

        elif button == self.TEAM2_READY and self.current_state == self.STATE_WAITING:
            self.team2_ready = True
            self.set_color(Color(0, 255, 0), 0)  # Зеленый на 2 секунды
            if self.team1_ready:
                self.current_state = self.STATE_READY

        elif button == self.REFEREE_START and self.current_state == self.STATE_READY:
            self.current_state = self.STATE_FIGHT
            playsound('//home//admin//project//buttons//start.mp3', block=False)
            self.fade_to_color(Color(255, 0, 0))  # Красный
            self.fight_started.emit()

        elif (button in [self.TEAM1_STOP, self.TEAM2_STOP, self.REFEREE_STOP]) and self.current_state != self.STATE_WAITING:
            self.reset_to_waiting()
            playsound('//home//admin//project//buttons//stop.mp3', block=False)
            self.fight_stopped.emit()

    def cleanup(self):
        self.set_color(Color(0, 0, 0))
        GPIO.cleanup()
