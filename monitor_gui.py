import psutil
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

plt.style.use("dark_background")

cpu_data = []
memory_data = []
download_data = []
upload_data = []
disk_data = []

prev_bytes_recv = psutil.net_io_counters().bytes_recv
prev_bytes_sent = psutil.net_io_counters().bytes_sent

def update_stats():
    global prev_bytes_recv, prev_bytes_sent

    current_bytes_recv = psutil.net_io_counters().bytes_recv
    current_bytes_sent = psutil.net_io_counters().bytes_sent

    download_speed = current_bytes_recv - prev_bytes_recv
    upload_speed = current_bytes_sent - prev_bytes_sent

    prev_bytes_recv = current_bytes_recv
    prev_bytes_sent = current_bytes_sent

    # Atualiza os valores na interface
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Atualiza os dados do gráfico
    cpu_data.append(cpu_usage)
    memory_data.append(memory_usage)
    download_data.append(download_speed)
    upload_data.append(upload_speed)
    disk_data.append(disk_usage)

    # Mantém apenas os últimos 20 pontos no gráfico
    if len(cpu_data) > 20:
        cpu_data.pop(0)
        memory_data.pop(0)
        download_data.pop(0)
        upload_data.pop(0)

    update_graph()
    root.after(1000, update_stats)

def update_graph():
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # CPU
    ax1.plot(cpu_data, label="CPU Usage (%)", color="red")
    ax1.set_ylim(0, 100)
    ax1.set_title(f"CPU: {cpu_data[-1]}%", color="white")
    ax1.legend(loc="upper left", facecolor="#333333", edgecolor="white")
    ax1.grid(True, color="#555555")
    ax1.xaxis.set_visible(False)

    # Memória e Disco
    ax2.plot(memory_data, label="Memory Usage (%)", color="green")
    ax2.plot(disk_data, label="Disk Usage (%)", color="purple")
    ax2.set_ylim(0, 100)
    ax2.set_title(f"Memory: {memory_data[-1]}%, Disk Usage: {disk_data[-1]}%", color="white")
    ax2.legend(loc="upper left", facecolor="#333333", edgecolor="white")
    ax2.grid(True, color="#555555")
    ax2.xaxis.set_visible(False)

    # Download e Upload
    ax3.plot([x * 8 / 1024 for x in download_data], label="Download Speed (kbps)", color="orange")
    ax3.plot([x * 8 / 1024 for x in upload_data], label="Upload Speed (kbps)", color="blue")
    ax3.set_title(f"Download: {round(download_data[-1] * 8 / 1024, 2)} kbps, Upload: {round(upload_data[-1] * 8 / 1024, 2)} kbps", color="white")
    ax3.legend(loc="upper left", facecolor="#333333", edgecolor="white")
    ax3.grid(True, color="#555555")
    ax3.xaxis.set_visible(False)

    canvas.draw()

# Cria a janela principal
root = tk.Tk()
root.title("System Monitor with Graphs")
root.configure(bg="#2b2b2b")
root.geometry("800x600")

# Torna a janela responsiva
root.rowconfigure(0, weight=1)  # Linha para os gráficos
root.columnconfigure(0, weight=1)  # Coluna para os gráficos

# Cria os gráficos usando Matplotlib
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 10))  # 3 linhas e 1 coluna
fig.tight_layout(pad=3.0)
fig.patch.set_facecolor("#2b2b2b")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky="nsew")

# Inicia a atualização dos dados
update_stats()

# Inicia o loop da interface gráfica
root.mainloop()