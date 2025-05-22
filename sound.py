import os
import subprocess
import time

FIFO = "/tmp/sound_pipe"
SOUND_FILE = "Timer_sound.wav"

def check_audio_file():
    """Проверяет, поддерживается ли файл"""
    try:
        # Проверка через ffprobe (из ffmpeg)
        cmd = f"ffprobe -v error -show_entries stream=codec_name {SOUND_FILE}"
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False

def play_sound():
    """Воспроизведение через aplay (надежнее pygame)"""
    subprocess.run(["aplay", SOUND_FILE])

if not check_audio_file():
    print("Ошибка: неподдерживаемый формат аудио!")
    exit(1)

if not os.path.exists(FIFO):
    os.mkfifo(FIFO, mode=0o666)

print("Сервер запущен. Ожидание сигналов...")
while True:
    try:
        with open(FIFO, 'r') as f:
            if f.read().strip() == "play":
                play_sound()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
