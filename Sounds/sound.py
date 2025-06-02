import os
import subprocess
import time
import threading

FIFO = "/tmp/sound_pipe"
START_FILE = "Sound/Start_sound.wav"
STOP_FILE = "Sound/Stop_sound.mp3"
READY_FILE = "Sound/Ready_sound.mp3"

sound_file = START_FILE


def check_audio_file():
    """Проверяет, поддерживается ли файл"""
    try:
        cmd = f"ffprobe -v error -show_entries stream=codec_name {sound_file}"
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False


def play_sound():
    """Воспроизведение через aplay"""
    subprocess.run(["aplay", sound_file])


def handle_signal():
    """Функция, которая запускается в потоке при сигнале"""
    threading.Thread(target=play_sound, daemon=True).start()


if not check_audio_file():
    print("Ошибка: неподдерживаемый формат аудио!")
    exit(1)

if not os.path.exists(FIFO):
    os.mkfifo(FIFO, mode=0o666)

print("Сервер запущен. Ожидание сигналов...")
while True:
    try:
        with open(FIFO, "r") as f:
            for line in f:
                if line.strip() == "start":
                    sound_file = START_FILE
                    handle_signal()
                elif line.strip() == "stop":
                    sound_file = STOP_FILE
                    handle_signal()
                elif line.strip() == "ready":
                    sound_file = READY_FILE
                    handle_signal()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
