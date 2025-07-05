import psutil
import subprocess
import time
import os
import signal

# Pingtunnel arguments
PINGTUNNEL_CMD = [
    "sudo", "./pingtunnel",
    "-type", "server",
    "-noprint", "1",
    "-nolog", "1"
]

CPU_THRESHOLD = 95  # percent
RAM_THRESHOLD = 12  # percent
CHECK_INTERVAL = 1  # seconds

def start_process():
    print("Starting pingtunnel...")
    return subprocess.Popen(
        PINGTUNNEL_CMD,
        preexec_fn=os.setsid  # Detach pingtunnel into a new process group
    )

def stop_process(_=None):
    print("Stopping all pingtunnel processes due to high resource usage...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info.get('name') or ""
            cmdline = proc.info.get('cmdline') or []
            if 'pingtunnel' in name or any('pingtunnel' in part for part in cmdline):
                print(f"Terminating pingtunnel (PID {proc.pid})...")
                proc.terminate()
                try:
                    proc.wait(timeout=1)
                except psutil.TimeoutExpired:
                    print(f"Force killing pingtunnel (PID {proc.pid})...")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


psutil.cpu_percent(interval=1)

def is_resource_high():
    cpu = psutil.cpu_percent(interval=None)  # non-blocking
    ram = psutil.virtual_memory().percent
    print(f"CPU: {cpu:.1f}%, RAM: {ram:.1f}%")
    return cpu >= CPU_THRESHOLD or ram >= RAM_THRESHOLD

def main():
    process = None
    try:
        process = start_process()
        while True:
            if is_resource_high():
                stop_process()
                while is_resource_high():
                    time.sleep(CHECK_INTERVAL)
                process = start_process()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stop_process()

if __name__ == "__main__":
    main()
