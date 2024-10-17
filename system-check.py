#! /usr/bin/env python3
""" Script to detect the operating system and its information """
import platform
import sys
import platform
import glob
import re
import subprocess
import health_checks
import time
import rich
from rich.progress import Progress

""" a module that checks, Memory utilization, Disk usage, CPU usage, and if a reboot is required for alinux system """

def system_info():
    info = platform.freedesktop_os_release()
    for key, val in info.items():
        rich.print(f"{key:>31} {"->|":4}{val}")
    return info["ID"]

def reboot_check():
    """ Checks the linux system for new kernel updates that require a reboot for full isntallations """
    now = platform.release()
    used = platform.release()
    now = re.search(r"([\d]{1,2}.[\d]{1,2}.[\d]{1,2})",now).group(1)
    kerns = glob.glob('/boot/vmlinu*')
    filtered = []
    for i in kerns:
        pattern = r"vmlinuz-([\d]{1,2}.[\d]{1,2}.[\d]{1,2}).*"
        res = re.search(pattern,i)
        if res != None: filtered.append(res.group(1))
        continue
    filtered = [list(map(int,x.split('.'))) for x in filtered]
    last = max(filtered)
    now = [int(x) for x in now.split('.')]
    print("Checking Reboot Requirement :")
    print(f"Reboot is Required! -> Kernel v{'.'.join([str(x) for x in last])} upgrade is Installed and Kernel v{'.'.join([str(x) for x in now])} is used." if last > now else "No Reboot is required at the moment.")
    latest = ".".join([str(x) for x in last])

if __name__ == "__main__":
    tasks = [
            {health_checks.App.init:f''},
            {reboot_check:f'{"-" * 20} REBOOT CHECK {"-" * 20}'},
            {system_info:f'{"-" * 20} Platform Information{"-" * 20}'}
    ]
    with Progress() as progress:
        bar = progress.add_task("[blue] Progress", total=len(tasks),start=True)
        for task in tasks:
            for check, msg in task.items():
                print(msg)
                check()
                progress.update(bar, advance=1)
