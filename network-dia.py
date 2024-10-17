import resource
import socket
# from scapy.all import sniff
import psutil

# Get network I/O statistics
# print(psutil.net_io_counters())


print(f"Memory usage: {usage.ru_maxrss} KB")

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr)
