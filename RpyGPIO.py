import asyncio
import RPi.GPIO as GPIO
from PyQt5.QtCore import QObject, pyqtSignal
from rpi_ws281x import PixelStrip, Color


class GPIOHandler(QObject):
    # Сигналы для внешних событий
    fight_started = pyqtSignal()
    fight_stopped = pyqtSignal()


    def __init__(self):
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

        super().__init__()
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False

        # Настройка пинов для кнопок
        self.TEAM1_READY = 13
        self.TEAM1_STOP = 6
        self.TEAM2_READY = 26
        self.TEAM2_STOP = 19
        self.REFEREE_START = 16
        self.REFEREE_STOP = 5

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

    async def stop(self):
        """Остановка обработки"""
        print("Stopping GPIO...")
        self._running = False  # Флаг для остановки цикла

        if self._task:
            self._task.cancel()  # Отменяем задачу
            try:
                await self._task  # Ждём завершения
            except asyncio.CancelledError:
                pass  # Ожидаемо, если задача отменена

        await self.set_color(Color(0, 0, 0))  # Выключаем светодиоды
        GPIO.cleanup()  # Освобождаем GPIO
        print("GPIO stopped.")

    async def run_loop(self):
        """Основной цикл обработки кнопок"""
        print("Starting!")
        try:
        # Инициализация - синий цвет
            await self.set_color(Color(0, 0, 255))

            while True:
                # Проверка всех кнопок
                for button in self.buttons:
                    if GPIO.input(button) == GPIO.HIGH:
                        await self.handle_button_press(button)
                        await asyncio.sleep(0.05)  # Задержка для антидребезга
                        print(self.current_state, self.team1_ready, self.team2_ready, button)

                await asyncio.sleep(0.05)

        except KeyboardInterrupt:
            await self.set_color(Color(0, 0, 0))  # Выключить все светодиоды
            GPIO.cleanup()
            print("Программа завершена.")

    async def handle_button_press(self, button):
        """Обработка нажатия кнопки"""
        if button == self.TEAM1_READY and self.current_state == self.STATE_WAITING:
            self.team1_ready = True
            await self.blink(Color(0, 255, 0), team=1, duration=2)  # Зеленый
            if self.team2_ready:
                self.current_state = self.STATE_READY

        elif button == self.TEAM2_READY and self.current_state == self.STATE_WAITING:
            self.team2_ready = True
            await self.blink(Color(0, 255, 0), team=2, duration=2)  # Зеленый
            if self.team1_ready:
                self.current_state = self.STATE_READY

        elif button == self.REFEREE_START:
            self.current_state = self.STATE_FIGHT
            self.fight_started.emit()
            await self.fade_to_color(Color(255, 0, 0), team=0, duration=2)  # Красный


        elif (button in [self.TEAM1_STOP, self.TEAM2_STOP, self.REFEREE_STOP]):
            self.fight_stopped.emit()
            await self.reset_to_waiting()


    async def set_color(self, color, team=0):
        """Установка цвета всей ленты"""
        if team == 1:
            for i in range(91, self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
        elif team == 2:
            for i in range(self.strip.numPixels()-90):
                self.strip.setPixelColor(i, color)
        else:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
        self.strip.show()
        # if duration > 0:
        #     await asyncio.sleep(duration)

    async def fade_to_color(self, target_color, team=0, duration=1.0):
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

            # for i in range(self.strip.numPixels()):
            #     self.strip.setPixelColor(i, Color(r, g, b))
            # self.strip.show()
            await self.set_color(Color(r, g, b), team=team)
            await asyncio.sleep(delay)

    async def blink(self, target_color, team=0, duration=2.0):
        """Мигание цветом"""
        current_color = self.strip.getPixelColor(0)
        await self.fade_to_color(target_color, team=team, duration=duration/2)
        await self.fade_to_color(current_color, team=team, duration=duration/2)

    async def reset_to_waiting(self):
        """Сброс в состояние ожидания"""
        self.current_state = self.STATE_WAITING
        self.team1_ready = False
        self.team2_ready = False
        await self.fade_to_color(Color(0, 0, 255))  # Синий

    async def stop(self):
        print("Stoping")
        await self.set_color(Color(0, 0, 0))
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        GPIO.cleanup()
