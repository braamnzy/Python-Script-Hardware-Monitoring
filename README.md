# Hardware Resource Monitor (PyMon)

Project ini adalah alat pemantauan sumber daya sistem *real-time* berbasis Python. Dikembangkan untuk memenuhi kebutuhan observasi penggunaan hardware (CPU, RAM, GPU, Disk, & Battery) secara dinamis dengan notifikasi dan logging otomatis.

## 🚀 Fitur Utama

* **Real-time Tracking:** Pemantauan metrik hardware setiap 5 detik (interval dapat disesuaikan).
* **Threshold Alert System:** Memberikan peringatan otomatis jika penggunaan CPU/RAM melebihi 85% atau Disk melebihi 90%.
* **Windows Notifications:** Notifikasi desktop menggunakan library `plyer` dengan cooldown system untuk mencegah spam.
* **CSV Data Logging:** Menyimpan riwayat monitoring ke file CSV untuk analisis lebih lanjut.
* **Cross-Hardware Support:** Mendukung pemantauan GPU menggunakan library `GPUtil` dan status baterai.
* **Error Handling:** Menggunakan blok `try-except` untuk memastikan skrip tetap berjalan meskipun terjadi kegagalan pembacaan sensor pada hardware tertentu.

## 🛠️ Tech Stack & Konsep Dasikom

Project ini mengimplementasikan beberapa konsep dasar sistem komputer:

* **Python 3**: Bahasa pemrograman utama.
* **Library psutil**: Digunakan untuk mengakses *system calls* dan statistik utilitas sistem (CPU, memori, disk, network, sensor).
* **Library GPUtil**: Digunakan untuk berinteraksi dengan driver kartu grafis.
* **Library plyer**: Untuk mengirim notifikasi native ke Windows.
* **CSV Module**: Untuk logging data terstruktur yang dapat dibuka di Excel/spreadsheet.
* **Operating System Abstraction**: Bagaimana software mengambil data dari kernel sistem operasi.

## 📋 Cara Penggunaan

1. Pastikan library yang dibutuhkan terinstall:
```bash
pip install psutil gputil plyer
```

2. Jalankan skrip:
```bash
python monitor.py
```

3. Monitor akan:
   - Menampilkan informasi sistem di terminal
   - Menyimpan log ke file `system_monitor_log.csv`
   - Mengirim notifikasi Windows jika ada threshold warning
   
4. Tekan `Ctrl + C` untuk menghentikan pemantauan.

## 📊 Output & File

### Terminal Output
```
===================================
Time : 2024-01-15 14:30:45
CPU  : 45.2%
RAM  : 62.8%
Disk : 75.3%
GPU  : 12.50%
Battery : 85%
```

### CSV Log File
File `system_monitor_log.csv` berisi:
- Timestamp
- CPU Usage (%)
- RAM Usage (%)
- Disk Usage (%)
- GPU Usage (%)
- Battery Level (%)

Data ini dapat dibuka dengan Excel atau digunakan untuk analisis dengan pandas.

## ⚙️ Konfigurasi

Anda dapat menyesuaikan beberapa parameter di dalam kode:
```python
# Interval monitoring (dalam detik)
monitor_system(interval=5)

# Threshold warning
CPU_THRESHOLD = 85  # %
RAM_THRESHOLD = 85  # %
DISK_THRESHOLD = 90  # %

# Cooldown notifikasi (dalam detik)
NOTIFICATION_COOLDOWN = 300  # 5 menit
```

## 🔔 Sistem Notifikasi

Notifikasi Windows akan muncul ketika:
- CPU usage > 85%
- RAM usage > 85%
- Disk usage > 90%

Notifikasi memiliki cooldown 5 menit untuk mencegah spam pada kondisi yang sama.

## 📁 Struktur Project
```
pymon/
│
├── PyMon.py              # Script utama
├── system_monitor_log.csv  # Log file (auto-generated)
├── README.md              # Dokumentasi
└── requirements.txt        # Library diperlukan
```

## 🔮 Roadmap & Fitur Potensial

Berikut adalah beberapa fitur yang sedang dipertimbangkan untuk pengembangan selanjutnya:

- [ ] Dashboard web real-time dengan Flask/FastAPI
- [ ] Alert via Email/Telegram Bot
- [ ] Historical data analysis & visualization
- [ ] Process monitoring (top CPU/RAM consumers)
- [ ] Network bandwidth monitoring
- [ ] Temperature monitoring (CPU/GPU)
- [ ] Auto-optimization features
- [ ] Multi-device monitoring support
- [ ] Configurable thresholds via config file
- [ ] Database integration (SQLite/PostgreSQL)

## ⚠️ Requirements

- **OS**: Windows (untuk notifikasi), Linux/macOS (tanpa notifikasi Windows)
- **Python**: 3.7+
- **GPU**: Optional (script tetap berjalan tanpa GPU)

## 🐛 Troubleshooting

### Notifikasi tidak muncul di Windows
- Pastikan notifikasi Windows tidak diblokir di Settings
- Check Windows Focus Assist settings

### Error "No module named 'plyer'"
```bash
pip install plyer
```

### GPU tidak terdeteksi
- Pastikan driver NVIDIA terinstall
- GPUtil hanya support NVIDIA GPU

## 👨‍💻 Author

Developed as a Hardware system information tool for modular use and further development.

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!