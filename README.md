# 🏠 KOST ELITE - Sistem Manajemen Kost & Properti

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Desktop%20(Windows%2FMac)-lightgrey)
![UI Framework](https://img.shields.io/badge/UI-CustomTkinter-blue)
![Architecture](https://img.shields.io/badge/Architecture-MVC%20Pattern-green)

**Kost Elite** adalah aplikasi desktop modern berbasis Python untuk membantu pemilik kost (Owner) mengelola properti, memantau ketersediaan kamar, dan mencatat data penghuni secara real-time. Dibangun dengan antarmuka **Dark Mode** yang elegan dan struktur kode profesional.

---

## ✨ Fitur Unggulan

### 1. 📊 Dashboard Interaktif
* **Statistik Real-time:** Menampilkan total kamar, kamar terisi, dan sisa kamar kosong secara otomatis.
* **Visual Grid Layout:** Representasi visual status kamar.
    * 🟩 **Hijau:** Kamar Kosong (Available).
    * 🟥 **Merah:** Kamar Terisi (Occupied).

### 2. 🛏️ Manajemen Data Kamar (CRUD)
* Tambah kamar baru dengan spesifikasi (Tipe, Harga, Nomor).
* Hapus data kamar dengan aman.
* Validasi otomatis (mencegah nomor kamar ganda).

### 3. 👥 Check-In Penghuni Cerdas
* Form input penghuni yang terintegrasi.
* **Smart Filtering:** Sistem hanya menampilkan kamar yang *Available* di menu pilihan.
* **Auto-Update Status:** Saat penghuni disimpan, status kamar otomatis berubah menjadi *Occupied*.

### 4. 🛡️ Database Otomatis (SQLite)
* Tidak perlu instalasi server database (XAMPP/MySQL).
* Database dan Tabel dibuat otomatis saat aplikasi pertama kali dijalankan (`Auto-Migration`).

---

## 📸 Screenshots

*(Silakan upload screenshot aplikasi Anda di sini agar terlihat menarik)*

| Dashboard Overview | Check-In Penghuni |
|:---:|:---:|
| ![Dashboard](https://via.placeholder.com/400x250?text=Upload+Screenshot+Dashboard) | ![Form](https://via.placeholder.com/400x250?text=Upload+Screenshot+Form) |

---

## 🛠️ Teknologi & Arsitektur

Aplikasi ini dibangun menggunakan pola desain **MVC (Model-View-Controller)** untuk memastikan kode bersih, mudah dibaca, dan mudah dikembangkan (Scalable).

* **Language:** Python 3.11
* **GUI Library:** CustomTkinter (Modern UI wrapper for Tkinter)
* **Database:** SQLite3
* **Struktur File:**

```bash
AplikasiKost_Python/
│
├── database/           # MODEL & CONTROLLER (Logic)
│   └── logic.py        # Menangani Query SQL & Transaksi Data
│
├── views/              # VIEW (Tampilan UI)
│   ├── dashboard_view.py
│   ├── rooms_view.py
│   ├── tenants_view.py
│   └── ...
│
├── main.py             # Entry Point (Navigasi Utama)
└── README.md           # Dokumentasi