import platform
import time
import os
import socket
import psutil

# Function to get CPU usage
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage

# Function to get memory usage
def get_memory_usage():
    mem = psutil.virtual_memory()
    total = mem.total / (1024.0 ** 3)  # Convert to GB
    used = mem.used / (1024.0 ** 3)  # Convert to GB
    percent = mem.percent
    return total, used, percent

# Function to get disk usage
def get_disk_usage():
    disk = psutil.disk_usage('/')
    total = disk.total / (1024.0 ** 3)  # Convert to GB
    used = disk.used / (1024.0 ** 3)  # Convert to GB
    percent = disk.percent
    return total, used, percent

# Function to get network statistics
def get_network_stats():
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent / (1024.0 ** 2)  # Convert to MB
    bytes_recv = net_io.bytes_recv / (1024.0 ** 2)  # Convert to MB
    packets_sent = net_io.packets_sent
    packets_recv = net_io.packets_recv
    return bytes_sent, bytes_recv, packets_sent, packets_recv


# Function to display CPU usage
def display_cpu_usage(cpu_usage):
    print('---------- CPU ----------')
    print(f"CPU Usage: {cpu_usage}%")
    print()

# Function to display memory usage
def display_memory_usage(total, used, percent):
    print('---------- RAM & Disk usage ----------')
    print(f"RAM Used: {used:.2f} GB / {total:.2f} GB ({percent}%)")
    print()

# Function to display disk usage
def display_disk_usage(total, used, percent):
    print(f"Disk Used: {used} GB / {total} GB ({percent}%)")
    print()

# Function to display network statistics
def display_network_stats(bytes_sent, bytes_recv, packets_sent, packets_recv):
    print('---------- Network stat ----------')
    print(f"Bytes Sent: {bytes_sent} MB")
    print(f"Bytes Received: {bytes_recv} MB")
    print(f"Packets Sent: {packets_sent}")
    print(f"Packets Received: {packets_recv}")
    print()

# Main loop to monitor system performance
while True:
    # Get CPU usage
    cpu_usage = get_cpu_usage()
    display_cpu_usage(cpu_usage)

    # Get memory usage
    total, used, percent = get_memory_usage()
    display_memory_usage(total, used, percent)

    # Get network statistics
    bytes_sent, bytes_recv, packets_sent, packets_recv = get_network_stats()
    display_network_stats(bytes_sent, bytes_recv, packets_sent, packets_recv)

    # Sleep for 1 second before next update
    time.sleep(1)
