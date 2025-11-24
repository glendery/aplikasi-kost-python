import customtkinter as ctk
from tkinter import messagebox
from database import logic

class RoomsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header
        ctk.CTkLabel(self, text="Manajemen Data Kamar", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # --- FORM TAMBAH KAMAR (HIJAU) ---
        form_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        form_frame.pack(fill="x", pady=(0, 10))
        form_frame.grid_columnconfigure((0,1,2), weight=1)

        ctk.CTkLabel(form_frame, text="Nomor Kamar (Range: 1-10):").grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.entry_no = ctk.CTkEntry(form_frame, placeholder_text="Cth: 101 atau 1-10")
        self.entry_no.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkLabel(form_frame, text="Tipe Kamar:").grid(row=0, column=1, padx=15, pady=5, sticky="w")
        self.combo_type = ctk.CTkOptionMenu(form_frame, values=["AC", "Non AC"]) 
        self.combo_type.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkLabel(form_frame, text="Harga (Rp):").grid(row=0, column=2, padx=15, pady=5, sticky="w")
        self.entry_price = ctk.CTkEntry(form_frame, placeholder_text="Cth: 1500000")
        self.entry_price.grid(row=1, column=2, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkButton(form_frame, text="+ TAMBAH KAMAR", fg_color="#2ecc71", command=self.add_room_action).grid(row=2, column=0, columnspan=3, padx=15, pady=15, sticky="ew")

        # --- FORM HAPUS MASSAL (MERAH - BARU!) ---
        delete_frame = ctk.CTkFrame(self, fg_color="#3a1c1c", border_color="#e74c3c", border_width=1) # Warna merah gelap
        delete_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(delete_frame, text="Hapus Massal (Pisahkan dengan koma):", text_color="#ffadad").pack(side="left", padx=15, pady=10)
        
        self.entry_delete = ctk.CTkEntry(delete_frame, placeholder_text="Cth: 101, 102, 105", width=300)
        self.entry_delete.pack(side="left", padx=5, pady=10)
        
        ctk.CTkButton(delete_frame, text="🗑️ HAPUS SEKALIGUS", fg_color="#e74c3c", hover_color="#c0392b", 
                      command=self.delete_mass_action).pack(side="left", padx=15, pady=10)

        # --- TABEL ---
        self.load_table()

    def load_table(self):
        if hasattr(self, 'list_container'): 
            self.list_container.destroy()
        
        ctk.CTkLabel(self, text="List Kamar Terdaftar", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(10, 5))
        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(fill="x")

        # Header
        header = ctk.CTkFrame(self.list_container, height=35, fg_color="gray25")
        header.pack(fill="x", pady=2)
        headers = [("No. Kamar", 100), ("Tipe", 200), ("Harga", 150), ("Status", 100), ("Aksi", 100)]
        for t, w in headers:
             ctk.CTkLabel(header, text=t, width=w, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)

        # Data Rows
        rooms = logic.get_all_rooms()
        try:
            rooms.sort(key=lambda x: int(x[1])) 
        except:
            rooms.sort(key=lambda x: x[1])

        if not rooms:
             ctk.CTkLabel(self.list_container, text="Belum ada data kamar.").pack(pady=20)
             return

        for r in rooms:
            row = ctk.CTkFrame(self.list_container, height=40, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=r[1], width=100).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=r[2], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"Rp {r[3]:,}", width=150).pack(side="left", padx=5)
            
            status_color = "#2ecc71" if r[4] == 'Available' else "#e74c3c"
            ctk.CTkLabel(row, text=r[4], text_color=status_color, width=100, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            
            ctk.CTkButton(row, text="Hapus", width=80, height=25, fg_color="transparent", border_color="#e74c3c", border_width=1, text_color="#e74c3c", 
                          command=lambda id=r[0]: self.delete_room_action(id)).pack(side="left", padx=5)

    def add_room_action(self):
        input_no = self.entry_no.get()
        input_price = self.entry_price.get()
        input_type = self.combo_type.get()

        if not input_no or not input_price:
            messagebox.showwarning("Warning", "Data tidak lengkap!")
            return

        # LOGIKA INPUT RANGE (1-10)
        if "-" in input_no:
            try:
                parts = input_no.split("-")
                start = int(parts[0])
                end = int(parts[1])
                count_success = 0
                for i in range(start, end + 1):
                    try:
                        logic.add_room(str(i), input_type, input_price)
                        count_success += 1
                    except: pass
                messagebox.showinfo("Sukses", f"Berhasil menambah {count_success} kamar!")
            except:
                messagebox.showerror("Error", "Format range salah! Gunakan: 1-10")
        else:
            try:
                logic.add_room(input_no, input_type, input_price)
                messagebox.showinfo("Sukses", "Kamar ditambahkan!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.load_table()
        self.entry_no.delete(0, "end")

    # --- LOGIKA HAPUS MASSAL (BARU) ---
    def delete_mass_action(self):
        raw_input = self.entry_delete.get()
        
        if not raw_input:
            messagebox.showwarning("Peringatan", "Isi nomor kamar yang mau dihapus!")
            return

        if not messagebox.askyesno("Konfirmasi Ekstrem", f"Yakin ingin menghapus kamar: {raw_input}?"):
            return

        # Pecah string "1, 5, 6" menjadi list ['1', '5', '6']
        # .split(",") memisahkan koma
        # .strip() membuang spasi jika user mengetik "1, 5" (ada spasi)
        room_list = [x.strip() for x in raw_input.split(",")]
        
        count = 0
        for r_num in room_list:
            if r_num: # Cek agar string kosong tidak terproses
                logic.delete_room_by_number(r_num)
                count += 1
        
        messagebox.showinfo("Selesai", f"{count} Kamar telah dihapus.")
        self.load_table() # Refresh tabel
        self.entry_delete.delete(0, "end") # Bersihkan input

    def delete_room_action(self, room_id):
        if messagebox.askyesno("Konfirmasi", "Hapus kamar ini?"):
            logic.delete_room(room_id)
            self.load_table()