
# 📘 Sistem Absensi I/O Multiplexing (GUI)

## 🎯 Deskripsi
Sistem ini adalah aplikasi absensi sederhana menggunakan Python:
- Server dapat mendengarkan banyak klien sekaligus dengan I/O Multiplexing (`select`)
- Client dapat melakukan absen dan melihat rekap absensinya
- Tersedia GUI untuk siswa & admin (menggunakan Tkinter)

---

## 🖥️ Fitur

### Server (server_gui_absen.py)
✅ GUI real-time menampilkan daftar hadir  
✅ Mencatat waktu absen otomatis  
✅ Mencegah absen lebih dari 1x  
✅ Ekspor ke Excel  
✅ Filter absensi berdasarkan jam  
✅ Reset otomatis setiap jam 00:00  
✅ Edit data absensi langsung dari tabel

### Client (client_gui_absen.py)
✅ Input nama untuk absen  
✅ Balasan langsung dari server  
✅ Menyimpan bukti absen ke file lokal  
✅ Bisa melihat rekap absen kapan saja

## 
- Validasi agar tidak bisa absen 2x
- Auto-save ke Excel
- Auto-reset harian pukul 00:00
- Bisa lihat rekap pribadi

---

## 📂 Struktur Folder

```
├── src/
│ ├── main_login.py
│ ├── client_gui_absen.py
│ └── server_gui_absen.py
├── data/
│  ├──absensi.xlsx
|  └── daftar_absen.txt
├── .gitignore
├── config.txt
├── requirements.txt
└── README.pdf
```

---

## 🚀 Cara Menjalankan

1. Buka terminal

2. Aktifkan virtual environment (opsional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. install dependensi:
```bash
pip install openpyxl pillow
```

4. Jalankan program:
```bash
python3 src/main_login.py
```

5. Login.
Guru (Admin) → Masukkan password: admin123
Murid (Client) → Input nama lalu klik Kirim Absen

---

## 🛠️ Persyaratan

- Python 3.x
- Modul:
  - `tkinter` (built-in)
  - `openpyxl`
  - `socket`, `select`, `threading`

Install openpyxl:
```bash
pip install openpyxl
```

- pip install -r requirements.txt        # buat jalanin aja
- pip install -r dev-requirements.txt    # kalau mau build/bundling/develop

---

## 🔧 MAINTENANCE:
- Kalau file `absensi.xlsx` error → buat ulang file kosong dengan header: `Nama`, `Tanggal`, `Waktu`
- Kalau muncul error "File tidak ditemukan" → pastikan struktur folder `data/` dan `src/` benar
- Untuk fitur baru: cukup tambahkan fungsinya dan update juga di `README.md`

- Tapi... Kalau Masih Error "ModuleNotFoundError: No module named 'openpyxl'"(linux)

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/main_login.py

---

## ✅ STATUS AKHIR:
Semua sudah:
- 🔁 **Lintas platform siap (Windows/Linux/macOS)**
- 📁 Struktur folder sudah universal
- 📋 README dan `.gitignore` sudah aman

---

## 👏 Dibuat dengan semangat belajar dan semangat 9 tahun!

# Sistem Absensi Siswa (I/O Multiplexing)

## 📚 Fitur
- Login sebagai Guru (admin)
- Login sebagai Murid (client)
- Server mencatat absensi ke file Excel
- Client mengirim data absensi
- GUI bertema Pokémon White & Black Version

## 🛠 Cara Menjalankan
1. Jalankan `main_login.py`
2. Pilih login:
   - Guru → Password: `admin123`
   - Murid → Langsung input nama

## 📂 Struktur Folder
- src/: Source code Python
- assets/: Gambar dan icon
- data/: Data absensi (Excel, TXT)
- dist/: Hasil bundling .exe

## 🔑 Password Admin
- admid123