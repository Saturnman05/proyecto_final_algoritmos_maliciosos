from cloudinary import config as cloud_config
from cloudinary.uploader import upload
from datetime import datetime
from os import remove
from src.config import SAVE_PATH, USER_NAME, DEVICE_NAME, IP_ADDRESS, OS_NAME

cloud_config(
    cloud_name="dsnwguzkd",
    api_key="623166659259627",
    api_secret="hrxWwTWkKXg_tQYr-0NGlqsjWDE",
    secure=True,
)


def upload_to_cloudinary(filepath: str):
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
