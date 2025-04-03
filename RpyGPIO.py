import asyncio
import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, pyqtSignal
from rpi_ws281x import PixelStrip, Color


class GPIOHandler(QObject):
    # Сигналы для внешних событий
    fight_started = pyqtSignal()
    fight_stopped = pyqtSignal()

    # Настройки по умолчанию
    LED_COUNT = 180
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 255
    LED_INVERT = False
    LED_CHANNEL = 0

    # Состояния системы
    STATE_WAITING = 0
    STATE_READY = 1
    STATE_FIGHT = 2

    def __init__(self):
        super().__init__()
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False

        # Настройка пинов для кнопок
        self.TEAM1_READY = 6
        self.TEAM1_STOP = 5
        self.TEAM2_READY = 13
        self.TEAM2_STOP = 16
        self.REFEREE_START = 19
        self.REFEREE_STOP = 26

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

    # async def start(self):
    #     """Запуск основного цикла обработки"""
    #     if self._running:
    #         return

    #     self._running = True
    #     self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        """Остановка обработки"""
        self._running = False
        if self._task:
            await self._task
        await self.set_color(Color(0, 0, 0))  # Выключить светодиоды
        GPIO.cleanup()

    async def start(self):
        """Основной цикл обработки кнопок"""
        try:
        # Инициализация - синий цвет
            await self.set_color(Color(0, 0, 255))

            while True:
                # Проверка всех кнопок
                for button in self.buttons:
                    if GPIO.input(button) == GPIO.HIGH:
                        await self._handle_button_press(button)
                        await asyncio.sleep(0.1)  # Задержка для антидребезга
                        print(self.current_state, self.team1_ready, self.team2_ready, button)

                await asyncio.sleep(0.05)

        except KeyboardInterrupt:
            await self.set_color(Color(0, 0, 0))  # Выключить все светодиоды
            GPIO.cleanup()
            print("Программа завершена.")

    async def _handle_button_press(self, button):
        """Обработка нажатия кнопки"""
        if button == self.TEAM1_READY and self.current_state == self.STATE_WAITING:
            self.team1_ready = True
            await self.blink(Color(0, 255, 0), 2)  # Зеленый
            if self.team2_ready:
                self.current_state = self.STATE_READY

        elif button == self.TEAM2_READY and self.current_state == self.STATE_WAITING:
            self.team2_ready = True
            await self.blink(Color(0, 255, 0), 2)  # Зеленый
            if self.team1_ready:
                self.current_state = self.STATE_READY

        elif button == self.REFEREE_START and self.current_state == self.STATE_READY:
            self.current_state = self.STATE_FIGHT
            await self.fade_to_color(Color(255, 0, 0), 2)  # Красный
            self.fight_started.emit()

        elif (button in [self.TEAM1_STOP, self.TEAM2_STOP, self.REFEREE_STOP]) and self.current_state != self.STATE_WAITING:
            await self.reset_to_waiting()
            self.fight_stopped.emit()

    async def set_color(self, color, duration=0):
        """Установка цвета всей ленты"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        if duration > 0:
            await asyncio.sleep(duration)

    async def fade_to_color(self, target_color, duration=1.0):
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
            await asyncio.sleep(delay)

    async def blink(self, target_color, duration=2.0):
        """Мигание цветом"""
        current_color = self.strip.getPixelColor(0)
        await self.fade_to_color(target_color, duration/2)
        await self.fade_to_color(current_color, duration/2)

    async def reset_to_waiting(self):
        """Сброс в состояние ожидания"""
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        await self.fade_to_color(Color(0, 0, 255))  # Синий

    def stop(self):
        """Синхронная остановка обработчика"""
        self._running = False
        if self._task:
            self._task.cancel()
        self.strip.setPixelColor(0, Color(0, 0, 0))  # Выключить светодиоды
        self.strip.show()
        GPIO.cleanup()
