import argparse
import resource
import socket
import time
import signal
# from scapy.all import sniff
import psutil
from psutil import net_if_addrs
def signal_handler(signum, frame):
    print(f"Signal Number: {signum}, Frame: {frame}")
    # Add any custom processing here, such as cleaning up resources or exiting the program.

    print("Exiting...")
    exit(0)

# Get network I/O statistics

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)
net_stat = {}
net_io_counters = psutil.net_io_counters(pernic=True)
for interface, stats in net_io_counters.items():
    net_stat["Interface"] = {}
    net_stat['Interface']["MB Sent"] = f"{stats.bytes_sent / (1024 * 1024):.2f}"
    net_stat['Interface']["MB Received"] = f"{stats.bytes_recv / (1024 * 1024):.2f}"
    net_stat['Interface']["Packets Sent"]= f"{stats.packets_sent}"
    net_stat['Interface']["Packets Received"] = f"{stats.packets_recv}"
    net_stat['Interface']["Errors In"]= f"{stats.errin}"
    net_stat['Interface']["Errors Out"]= f"{stats.errout}"
    net_stat['Interface']["Drop In"]=  f"{stats.dropin}"
    net_stat['Interface']["Drop Out"]= f"{stats.dropout}"


def general_report():
    print("-------REPORT-------")
    for inet, details in net_stat.items():
        print(f"------------Netowrk interface {inet}----------")
        for stat, detail in details.items():
            print(f"{stat:>31} {"->|":4}{detail}")

pid = {}
addrs = {}


def monitor_network(interface):
    net_io_counters = psutil.net_io_counters(pernic=True)
    prev_bytes_sent = net_io_counters[interface].bytes_sent
    prev_bytes_recv = net_io_counters[interface].bytes_recv
    global pid
    global addrs
    accum = 0
    while True:
        accum +=1
        time.sleep(1)
        net_io_counters = psutil.net_io_counters(pernic=True)
        bytes_sent = net_io_counters[interface].bytes_sent - prev_bytes_sent
        bytes_recv = net_io_counters[interface].bytes_recv - prev_bytes_recv
        prev_bytes_sent = net_io_counters[interface].bytes_sent
        prev_bytes_recv = net_io_counters[interface].bytes_recv

        # print(f"Bytes Sent: {bytes_sent / (1024 * 1024)} MB/s, Bytes Received: {bytes_recv / (1024 * 1024)} MB/s")

        # Check network connections
        net_connections = psutil.net_connections()
        net_cons = len(net_connections)
        pid["Connections"] = net_cons
        for conn in net_connections:
            pid[f'{conn.pid}'] = {}
            pid[f'{conn.pid}']["Status"] = f"{conn.status}"
            pid[f'{conn.pid}']["Local Address"] = f"{conn.laddr}"
            pid[f'{conn.pid}']["Remote Address"] = f"{conn.raddr}"
        # Check network interface addresses
        net_if_addrs = psutil.net_if_addrs()
        nics = len(net_if_addrs)
        addrs["Network Interfaces"] = nics
        for addr in net_if_addrs[interface]:
            addrs["Family"] = {}
            addrs["Family"]["Name"] = f"{addr.family.name}"
            addrs["Family"]["Address"]= f"{addr.address}"
            addrs["Family"]["Netmask"] =  f"{addr.netmask}"
            addrs["Family"]["Broadcast"] = f"{addr.broadcast}"
        if accum == nics + net_cons:
            break

def net_report():
    print("-------REPORT-------")
    for proc,details in pid.items():
        print(f"------------ Process Network details {proc}----------")
        for field, info in details.items():
            print(f"{field:>31} {"->|":4}{info}")

    print("-------REPORT-------")
    for  family, detail in addrs.items():
        print(f"------------Network Family Details {family}----------")
        for field, info in detail.items():
            print(f"{field:>10} {"->|":4}{info}")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # parse = argparse.ArgumentParser(description="Network stats and Traffic report")
    # parse.add_argument('-c','--continuous',help='If set, it will monitor and report until stoped.')
    # args = parse.parse_args()
    interface = "virbr0"

    monitor_network(interface)
    general_report()
    net_report()
