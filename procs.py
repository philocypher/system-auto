import sys
import os
import psutil

def list_processes():
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            print(f"Process ID: {info['pid']}, Name: {info['name']}, Username: {info['username']}")
            print(f"CPU Percent: {info['cpu_percent']}, Memory Percent: {info['memory_percent']}")
            print("------------------------")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def get_process_info(pid):
    try:
        p = psutil.Process(pid)
        info = {
            'pid': p.pid,
            'name': p.name(),
            'username': p.username(),
            'cpu_percent': p.cpu_percent(interval=1),
            'cpu_times': p.cpu_times(),
            'memory_info': p.memory_info(),
            'memory_percent': p.memory_percent(),
            'io_counters': p.io_counters(),
            'connections': p.connections(),
            'status': p.status(),
            'create_time': p.create_time(),
            'environ': p.environ(),
            'cmdline': p.cmdline(),
            'cwd': p.cwd(),
            'exe': p.exe(),
            'open_files': p.open_files(),
            'num_threads': p.num_threads(),
            'num_ctx_switches': p.num_ctx_switches()
        }

        return info
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} does not exist.")
        return None


if __name__ == "__main__":
    list_processes()
    args = []
    process_info = {}
    if len(sys.argv) > 1:
        for i in range(len(sys.argv) + 1):
            if i == 1:
                continue
            try:
                arg = int(sys.argv[i-1])
                args.append(int(sys.argv[i-1]))
            except ValueError as e:
                print("ERROR: Enter a valid PID number.")
                sys.exit(1)
    if len(args) > 0:
        for pid in args:
            try:
                p = psutil.Process(pid)
                process_info = get_process_info(pid)
                for key, value in process_info.items():
                        if key == 'environ':
                            continue
                        print(f"{key}: {value}")
            except psutil.NoSuchProcess as e:
                        print(f"ERROR: {e.msg} {e.pid}")
                        exit(1)
    else:
            pid = os.getpid()  # Use the current process PID for demonstration
            process_info = get_process_info(pid)
            print("----------- Proc details-----------")
            for key, value in process_info.items():
                if key == 'environ':
                    continue
                print(f"{key}: {value}")
