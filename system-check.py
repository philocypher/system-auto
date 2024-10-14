""" Script to detect the operating system and its information """
import platform
import sys
import rich

## OS name and version 

def system_info():
    info = platform.freedesktop_os_release()
    for key, val in info.items():
        rich.print(f"{key:>31} {"->|":4}{val}")
    return info["ID"]

if __name__ == "__main__":
    system_info()
