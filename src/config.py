import requests

from os import getlogin
from platform import node, system

USER_NAME = getlogin()
DEVICE_NAME = node()

try:
    IP_ADDRESS = requests.get("https://api.ipify.org").text
except:
    IP_ADDRESS = "Unknown"

OS_NAME = system()
SAVE_PATH = f"C:/Users/{USER_NAME}/AppData/local/Temp"
