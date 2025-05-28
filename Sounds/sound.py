import os
import subprocess
import time
import threading

FIFO = "/tmp/sound_pipe"
START_FILE = "Timer_sound.wav"
STOP_FILE = "Stop_sound.mp3"
READY_FILE = "Ready_sound.mp3"

SOUND_FILE = START_FILE

def check_audio_file():
    """Проверяет, поддерживается ли файл"""
    try:
        cmd = f"ffprobe -v error -show_entries stream=codec_name {SOUND_FILE}"
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False

def play_sound():
    """Воспроизведение через aplay"""
    subprocess.run(["aplay", SOUND_FILE])

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
        with open(FIFO, 'r') as f:
            for line in f:
                if line.strip() == "start":
                    SOUND_FILE = START_FILE
                    handle_signal()
                elif line.strip() == "stop":
                    SOUND_FILE = STOP_FILE
                    handle_signal()
                elif line.strip() == "ready":
                    SOUND_FILE = READY_FILE
                    handle_signal()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
