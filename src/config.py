from os import getlogin
from platform import node, system
from socket import gethostbyname, gethostname

USER_NAME = getlogin()
DEVICE_NAME = node()

try:
    IP_ADDRESS = gethostbyname(gethostname())
except:
    IP_ADDRESS = "Unknown"

OS_NAME = system()
SAVE_PATH = f"C:/Users/{USER_NAME}/AppData/local/Temp"
