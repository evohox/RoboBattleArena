import socketio
import os
from dotenv import load_dotenv
from typing import Dict, Any


class Tournament:
    def __init__(self, api_url):
        self.api_url = api_url
        self.sio = socketio.Client()
        self.is_connected = False

        # Регистрация обработчиков событий
        self.register_handlers()

        # Подключение к серверу и авторизация
        self.connect()
        self.teams_names = ["", ""]

    def register_handlers(self):
        """Регистрирует все обработчики событий."""

        @self.sio.event
        def connect():
            print("✅ Подключено к серверу.")
            self.is_connected = True

        @self.sio.event
        def disconnect():
            print("❌ Отключено от сервера.")
            self.is_connected = False

        # ID поединка
        @self.sio.on("BACK-END: Fight ID sent.")
        def get_fight_id(id):
            self.id = id
            print(f"ID поединка: {id}")

        @self.sio.on("BACK-END: Overlay data sent")
        def handle_external_data(data):
            print("[proxy] Получены данные:", data)
            try:
                self.teams_names = self.process_overlay_data(data)
                print("Названия команд: ", self.teams_names)

            except Exception as e:
                print("[timer] Ошибка при парсинге:", e)

    def process_overlay_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return [raw_data.get("team1", "Команда 1"), raw_data.get("team2", "Команда 2")]

    def connect(self):
        """Подключается к серверу."""
        try:
            self.sio.connect(self.api_url, wait_timeout=10)
            self.is_connected = True
        except Exception as e:
            print(f"⚠️ Не удалось подключиться: {e}")
            self.is_connected = False

    def send_team1_ready(self):
        """Отправляет готовность команды 1."""
        if self.is_connected:
            self.sio.emit("BUTTONS: Team 1 ready.", self.id)

    def send_team2_ready(self):
        """Отправляет готовность команды 2."""
        if self.is_connected:
            self.sio.emit("BUTTONS: Team 2 ready.", self.id)

    def send_fight_start(self):
        """Отправляет запрос на начало боя."""
        if self.is_connected:
            self.sio.emit("BUTTONS: Fight start.", self.id)

    def send_fight_end(self):
        """Отправляет запрос на завершение боя."""
        if self.is_connected:
            self.sio.emit("BUTTONS: Fight end.", self.id)

    def send_preparing(self):
        """Отправляет запрос на подготовку к бою."""
        if self.is_connected:
            self.sio.emit("BUTTONS: Preparing start.", self.id)

    def get_team_names(self):
        return self.teams_names

    def disconnect(self):
        """Отключается от сервера."""
        if self.is_connected:
            self.sio.disconnect()


# Пример использования
if __name__ == "__main__":
    load_dotenv()
    api_url = os.getenv("API_URL")
    tournament = Tournament(api_url=api_url)
