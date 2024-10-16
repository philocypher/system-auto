#! /usr/bin/env python3
# Chceking System and computer health.
import shutil
import argparse

#Third-party imports.
import psutil

def check_disk(path='/'):
    '''
    Checks Disk Usage and returns Free space in percentage.
    Takes in a parameter 'path' to the disk.
    '''
    try:
        disk_use = shutil.disk_usage(path)
        free_disk = disk_use.free / disk_use.total
        print(f"Disk Usage: {free_disk:.2%} is free")
        if (free_disk * 100) < 20:
            print(f" Disk free space is low!")
    except TypeError:
        print("Error: Set correct Path  with -p to calculate free space")

def cpu_usage(interval=None, percpu=False):
    """
    checks for cpu utilization in intervals.
    Takes in two parameters, intervals & percpu to check a single or all cpus.
    """
    if percpu is True and interval is not None:
        for _ in range(10):
            print('Each CPU Util per interval:',psutil.cpu_percent(interval=interval,percpu=True))
    if interval != None and percpu == False:
        cpu = psutil.cpu_percent(interval=interval,percpu=False)
        return cpu
    # if no arguement is provided, this is the Default.
    if interval is not None or not percpu:
        cpu = psutil.cpu_percent(1)
        if cpu > 75:
            print(f"Warnning! {cpu}% \n CPU Usage is High!")
        else:
            for _ in range(5):
                print(f"CPU Utilization in five intervals of 1 sec: {psutil.cpu_percent(1)}%")

class App:
    '''
    initializer class
    '''
    @staticmethod
    def init():
        # initialize the CLI arguement, intervals, all cpus, path
        parser = argparse.ArgumentParser(description="Checking CPU health and Disk space.")
        parser.add_argument('-i','--intervals',help='Set intervals to check CPU util upon it, min is 0.1')
        parser.add_argument('-p','--path',help='Path to check the disk free space.')
        parser.add_argument('-a','--all',help='If set, all CPU cores will be checked.')
        args = parser.parse_args()

        # Executing the tasks
        # if args are passed.
        if args.path != None:
            check_disk(args.path)
        # if path is not passed, default to main disk.
        else:
            check_disk()
        # if intervals and percpu are provided.
        if args.all is not '' and args.intervals is not None:
            cpu_usage(int(args.intervals),True)
        else:
            cpu_usage()

if __name__ == "__main__":
    print('Starting ...')
    App.init()
