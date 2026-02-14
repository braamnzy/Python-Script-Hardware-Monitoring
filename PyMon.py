import psutil
import GPUtil
import time
from datetime import datetime
from plyer import notification
import csv
import os

print("Script started...")

# Konfigurasi
CSV_FILE = "system_monitor_log.csv"
NOTIFICATION_COOLDOWN = 300  # 5 menit cooldown untuk notifikasi yang sama

# Tracking notifikasi terakhir
last_notification = {
    "cpu": 0,
    "ram": 0,
    "disk": 0
}

def initialize_csv():
    """Inisialisasi file CSV jika belum ada"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'CPU %', 'RAM %', 'Disk %', 'GPU %', 'Battery %'])
        print(f"✓ CSV log file created: {CSV_FILE}")

def log_to_csv(data):
    """Menyimpan data ke CSV"""
    try:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                data['timestamp'],
                data['cpu_percent'],
                data['ram_percent'],
                data['disk_percent'],
                data['gpu_percent'],
                data['battery_percent'] if data['battery_percent'] is not None else 'N/A'
            ])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def send_notification(title, message, alert_type):
    """Mengirim notifikasi Windows dengan cooldown"""
    current_time = time.time()
    
    # Cek cooldown
    if current_time - last_notification.get(alert_type, 0) < NOTIFICATION_COOLDOWN:
        return
    
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="System Monitor",
            timeout=10
        )
        last_notification[alert_type] = current_time
    except Exception as e:
        print(f"Error sending notification: {e}")

def get_system_info():
    try:
        GLOBAL_CPU_LOAD = psutil.cpu_percent()
        GLOBAL_RAM = psutil.virtual_memory().percent
        GLOBAL_DISK = psutil.disk_usage('C:\\').percent
        
        GLOBAL_GPU = GPUtil.getGPUs()
        GLOBAL_GPU_LOAD = GLOBAL_GPU[0].load * 100 if GLOBAL_GPU else 0
        
        GLOBAL_BATTERY = psutil.sensors_battery()
        GLOBAL_BATTERY_PERCENT = GLOBAL_BATTERY.percent if GLOBAL_BATTERY else None
        
        TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "timestamp": TIMESTAMP,
            "cpu_percent": GLOBAL_CPU_LOAD,
            "ram_percent": GLOBAL_RAM,
            "disk_percent": GLOBAL_DISK,
            "gpu_percent": GLOBAL_GPU_LOAD,
            "battery_percent": GLOBAL_BATTERY_PERCENT
        }

    except Exception as e:
        print(f"Error retrieving system info: {e}")
        return None

def check_and_alert(data):
    """Mengecek threshold dan mengirim notifikasi"""
    if data['cpu_percent'] > 85:
        print("⚠ WARNING: High CPU Usage!")
        send_notification(
            "⚠ High CPU Usage",
            f"CPU usage is at {data['cpu_percent']:.1f}%",
            "cpu"
        )
    
    if data['ram_percent'] > 85:
        print("⚠ WARNING: High RAM Usage!")
        send_notification(
            "⚠ High RAM Usage",
            f"RAM usage is at {data['ram_percent']:.1f}%",
            "ram"
        )
    
    if data['disk_percent'] > 90:
        print("⚠ WARNING: Disk Almost Full!")
        send_notification(
            "⚠ Disk Almost Full",
            f"Disk usage is at {data['disk_percent']:.1f}%",
            "disk"
        )

def monitor_system(interval=5):
    initialize_csv()
    print(f"✓ Logging to: {CSV_FILE}")
    print(f"✓ Monitoring interval: {interval} seconds")
    print("✓ Press Ctrl+C to stop\n")
    
    try:
        while True:
            data = get_system_info()
            
            if data:
                print("===================================")
                print(f"Time : {data['timestamp']}")
                print(f"CPU  : {data['cpu_percent']}%")
                print(f"RAM  : {data['ram_percent']}%")
                print(f"Disk : {data['disk_percent']}%")
                print(f"GPU  : {data['gpu_percent']:.2f}%")

                if data['battery_percent'] is not None:
                    print(f"Battery : {data['battery_percent']}%")
                else:
                    print("Battery : Not Available")

                # Cek threshold dan kirim notifikasi
                check_and_alert(data)
                
                # Simpan ke CSV
                log_to_csv(data)
            
            time.sleep(interval)
        
    except KeyboardInterrupt:
        print("\n✓ Monitoring stopped by user.")
        print(f"✓ Log saved to: {CSV_FILE}")

if __name__ == "__main__":
    monitor_system(interval=5)