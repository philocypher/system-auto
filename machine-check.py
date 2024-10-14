import shutil
import psutil


def disk_check(partition='/'):
    du = shutil.disk_usage(partition)
    free_in_gb = du.free / 2**30
    free_in_gb = round(free_in_gb)
    free_percentage = round(du.free / du.total * 100)
    return free_in_gb, free_percentage, round(du.total / 2**30)

def main():
    free_gb,free_percent, total_disk_space = disk_check()
    print(f"Free Disk Space: {free_gb}GB, %{free_percent} of Total {total_disk_space}GB space used")


if __name__ == "__main__":
    main()
