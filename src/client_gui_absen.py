import socket
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 9000

def kirim_absen():
    nim = entry_nim.get().strip()
    if not nim:
        messagebox.showwarning("Peringatan", "NIM harus diisi.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(nim.encode())
        response = client_socket.recv(1024).decode()
        messagebox.showinfo("Status Absen", response)
        client_socket.close()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal terhubung ke server:\n{e}")

# GUI
window = tk.Tk()
window.title("Client Absensi Mahasiswa")
window.geometry("350x150")

label_nim = tk.Label(window, text="Masukkan NIM:")
label_nim.pack(pady=5)

entry_nim = tk.Entry(window)
entry_nim.pack(pady=5)

btn_absen = tk.Button(window, text="Absen", command=kirim_absen)
btn_absen.pack(pady=10)

window.mainloop()
