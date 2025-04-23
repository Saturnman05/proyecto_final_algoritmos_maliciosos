import pyautogui
from datetime import datetime
from os import path, makedirs
from time import sleep
from src.config import SAVE_PATH
from src.uploader import upload_to_cloudinary
from src.activity_monitor import user_is_active

INTERVAL = 5
makedirs(SAVE_PATH, exist_ok=True)


def take_screenshot():
    while True:
        if not user_is_active():
            print("[…] Usuario inactivo, no se toma screenshot.")
            sleep(INTERVAL)
            continue

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        filepath = path.join(SAVE_PATH, filename)

        screenshot = pyautogui.screenshot().convert("RGB")
        screenshot.save(filepath, "JPEG", quality=70, optimize=True)

        upload_to_cloudinary(filepath)
        print(f"[✔] Screenshot tomada por actividad: {filename}")
        sleep(INTERVAL)
