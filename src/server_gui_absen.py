import socket
import select
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import threading
import csv
import os
import openpyxl

# === Konfigurasi ===
HOST = '127.0.0.1'
PORT = 9000
REKAP_FOLDER = "rekap"

# === Inisialisasi Socket ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
sockets_list = [server_socket]

# === Data Absensi & Mahasiswa ===
absensi = {}  # NIM -> (Nama, Waktu)
mahasiswa = {}  # NIM -> Nama

# === Baca Daftar Mahasiswa ===
daftar_file = "daftar_mahasiswa.csv"
if os.path.exists(daftar_file):
    with open(daftar_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mahasiswa[row['NIM']] = row['Nama']

# === Buat Folder Rekap Jika Belum Ada ===
if not os.path.exists(REKAP_FOLDER):
    os.makedirs(REKAP_FOLDER)

# === Fungsi Simpan Rekap ===
def simpan_rekap():
    tanggal = datetime.now().strftime('%Y-%m-%d')
    filename = f"{REKAP_FOLDER}/rekap_absensi_{tanggal}.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sudah Absen"
    ws.append(["NIM", "Nama", "Waktu Absen"])
    for nim, (nama, waktu) in absensi.items():
        ws.append([nim, nama, waktu])
    ws2 = wb.create_sheet("Belum Absen")
    ws2.append(["NIM", "Nama"])
    for nim in mahasiswa:
        if nim not in absensi:
            ws2.append([nim, mahasiswa[nim]])
    wb.save(filename)
    messagebox.showinfo("Rekap Disimpan", f"File: {filename}")

# === Fungsi Update Daftar Belum Absen ===
def update_belum_absen():
    for item in tree_belum_absen.get_children():
        tree_belum_absen.delete(item)
    for nim in mahasiswa:
        if nim not in absensi:
            tree_belum_absen.insert("", tk.END, values=(nim, mahasiswa[nim]))

# === Fungsi Lihat Rekap Tersimpan ===
def lihat_rekap():
    top = tk.Toplevel(window)
    top.title("📂 Rekap Absensi Sebelumnya")
    top.geometry("400x300")

    listbox = tk.Listbox(top)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    files = sorted([
        f for f in os.listdir(REKAP_FOLDER) if f.endswith(".xlsx")
    ])

    if not files:
        listbox.insert(tk.END, "(Belum ada rekap tersimpan)")
    else:
        for file in files:
            listbox.insert(tk.END, file)

    def buka_file():
        selection = listbox.curselection()
        if selection:
            filename = files[selection[0]]
            filepath = os.path.join(REKAP_FOLDER, filename)
            try:
                os.startfile(filepath)  # Hanya Windows
            except Exception as e:
                messagebox.showerror("Gagal membuka", str(e))

    btn_buka = tk.Button(top, text="Buka File", command=buka_file)
    btn_buka.pack(pady=5)

# === GUI Tkinter ===
window = tk.Tk()
window.title("Server Absensi Mahasiswa")
window.geometry("750x650")

label1 = tk.Label(window, text="✅ Mahasiswa yang Sudah Absen", font=("Arial", 12, "bold"))
label1.pack(pady=(10, 0))

tree_absen = ttk.Treeview(window, columns=("nim", "nama", "waktu"), show="headings", height=8)
tree_absen.heading("nim", text="NIM")
tree_absen.heading("nama", text="Nama")
tree_absen.heading("waktu", text="Waktu Absen")
tree_absen.pack(fill=tk.X, padx=10)

label2 = tk.Label(window, text="❌ Mahasiswa yang Belum Absen", font=("Arial", 12, "bold"))
label2.pack(pady=(20, 0))

tree_belum_absen = ttk.Treeview(window, columns=("nim", "nama"), show="headings", height=8)
tree_belum_absen.heading("nim", text="NIM")
tree_belum_absen.heading("nama", text="Nama")
tree_belum_absen.pack(fill=tk.X, padx=10)

# === Tombol Input Daftar Mahasiswa ===
def input_mahasiswa():
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        with open(file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mahasiswa[row['NIM']] = row['Nama']
        with open(daftar_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["NIM", "Nama"])
            writer.writeheader()
            for nim, nama in mahasiswa.items():
                writer.writerow({"NIM": nim, "Nama": nama})
        update_belum_absen()
        messagebox.showinfo("Berhasil", "Daftar mahasiswa diperbarui.")

# === Tombol ===
btn_frame = tk.Frame(window)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="📝 Input Daftar Mahasiswa", command=input_mahasiswa).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="💾 Simpan Rekap Hari Ini", command=simpan_rekap).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="📂 Lihat Rekap Sebelumnya", command=lihat_rekap).pack(side=tk.LEFT, padx=5)

# === Terima Koneksi Client ===
def handle_client():
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        for sock in read_sockets:
            if sock == server_socket:
                client_socket, _ = server_socket.accept()
                sockets_list.append(client_socket)
            else:
                try:
                    data = sock.recv(1024).decode()
                    nim = data.strip()
                    waktu = datetime.now().strftime("%H:%M:%S")
                    if nim in mahasiswa:
                        if nim not in absensi:
                            nama = mahasiswa[nim]
                            absensi[nim] = (nama, waktu)
                            tree_absen.insert("", tk.END, values=(nim, nama, waktu))
                            update_belum_absen()
                            sock.send("Absen berhasil".encode())
                        else:
                            sock.send("NIM sudah absen".encode())
                    else:
                        sock.send("NIM tidak terdaftar".encode())
                except:
                    sockets_list.remove(sock)
                    sock.close()

threading.Thread(target=handle_client, daemon=True).start()
update_belum_absen()
window.mainloop()
