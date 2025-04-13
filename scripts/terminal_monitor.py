## Programa para monitorar o uso de CPU, memória, disco e internet do sistema linux

import psutil
import os
import time

prev_bytes_recv = psutil.net_io_counters().bytes_recv
prev_bytes_sent = psutil.net_io_counters().bytes_sent

while True:
    os.system('clear')

    current_bytes_recv = psutil.net_io_counters().bytes_recv
    current_bytes_sent = psutil.net_io_counters().bytes_sent


    download_speed = current_bytes_recv - prev_bytes_recv
    upload_speed = current_bytes_sent - prev_bytes_sent
    prev_bytes_recv = current_bytes_recv
    prev_bytes_sent = current_bytes_sent

    print(f"CPU usage: {psutil.cpu_percent()} %")
    print(f"Memory usage: {psutil.virtual_memory().percent} %")
    print(f"Disk usage: {psutil.disk_usage('/').percent} %")
    print(f"Internet usage (Download): {download_speed} bytes/s")
    print(f"Internet usage (Upload): {upload_speed} bytes/s")
    
    time.sleep(1)
