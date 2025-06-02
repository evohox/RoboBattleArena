from rpi_ws281x import PixelStrip, Color
import threading
import time

class LEDController:
    """Класс для работы с эффектами светодиодной ленты."""

    def __init__(self, led_count=180, led_pin=18, brightness=255, freq_hz=800000, dma=10, invert=False, channel=0):
        """Инициализация светодиодной ленты
        Args:
            led_count (int, optional): Кол-во светодиодов в ленте. Defaults to 180.
            led_pin (int, optional): Номер порта GPIO, к которому подключена лента. Defaults to 18.
            brightness (int, optional): Яркость. Defaults to 255.
            freq_hz (int, optional): Частота (HZ). Defaults to 800000.
            dma (int, optional): Номер dma, используемый для передачи данных драйвера на светодиоды. Defaults to 10.
            invert (bool, optional): Следует ли инвертировать выходной сигнал. Defaults to False.
            channel (int, optional): Канал. Defaults to 0.
        """
        self.LED_COUNT = led_count
        self.lock = threading.Lock()

        self.strip = PixelStrip(
            led_count, led_pin, freq_hz, dma, invert, brightness, channel
        )
        self.strip.begin()

    def set_color(self, color: Color, team=0):
        """Покраска ленты в определенный цвет
        Args:
            color (Color): Цвет для покраски.
            team (int, optional): Номер команды (половины ленты). Defaults to 0.
        """
        with self.lock:
            if team == 1:
                for i in range(90, self.strip.numPixels()):
                    self.strip.setPixelColor(i, color)
            elif team == 2:
                for i in range(self.strip.numPixels() - 90):
                    self.strip.setPixelColor(i, color)
            else:
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, color)
            self.strip.show()

    def fade_to_color(self, target_color: Color, team=0, duration=0.5):
        """Плавный переход к цвету
        Args:
            target_color (Color): Желаемый цвет.
            team (int, optional): Номер команды (половины ленты). Defaults to 0.
            duration (float, optional): Продолжительность смены цвета. Defaults to 0.5.
        """
        steps = 100
        delay = duration / steps

        if team == 2:
            current_color = self.strip.getPixelColor(0)
        else:
            current_color = self.strip.getPixelColor(91)

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

            self.set_color(Color(r, g, b), team=team)
            time.sleep(delay)

    def circle_color(self, first_color: Color, second_color: Color, state_checker: function, frequency: int=100):
        """Движение бегущей строки
        Args:
            first_color (Color): Основной цвет.
            second_color (Color): Вторичный цвет.
            state_checker (function): Функция для остановки эффекта.
            frequency (int, optional): Частота. Defaults to 100.
        """
        delay = 1 / frequency
        half = self.LED_COUNT // 2
        band_width = 20
        line_id1 = 0
        line_id2 = 0

        while state_checker():
            for i in range(self.LED_COUNT):
                if i < half:
                    pos = (i - line_id1) % half
                    color = first_color if pos < band_width else Color(0, 0, 0)
                else:
                    pos = ((i - half) - line_id2) % half
                    color = second_color if pos < band_width else Color(0, 0, 0)
                self.strip.setPixelColor(i, color)
            self.strip.show()
            line_id1 = (line_id1 + 1) % half
            line_id2 = (line_id2 + 1) % half
            time.sleep(delay)
