import customtkinter as ctk
from tkinter import messagebox
from database import logic

class RoomsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header
        ctk.CTkLabel(self, text="Manajemen Data Kamar", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Form
        form_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        form_frame.pack(fill="x", pady=(0, 20))
        form_frame.grid_columnconfigure((0,1,2), weight=1)

        ctk.CTkLabel(form_frame, text="Nomor Kamar:").grid(row=0, column=0, padx=15, pady=5, sticky="w")
        self.entry_no = ctk.CTkEntry(form_frame, placeholder_text="Cth: 105")
        self.entry_no.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkLabel(form_frame, text="Tipe Kamar:").grid(row=0, column=1, padx=15, pady=5, sticky="w")
        self.combo_type = ctk.CTkOptionMenu(form_frame, values=["Standard (AC)", "Ekonomi (Non-AC)", "VIP", "Suite"])
        self.combo_type.grid(row=1, column=1, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkLabel(form_frame, text="Harga (Rp):").grid(row=0, column=2, padx=15, pady=5, sticky="w")
        self.entry_price = ctk.CTkEntry(form_frame, placeholder_text="Cth: 1500000")
        self.entry_price.grid(row=1, column=2, padx=15, pady=(0, 15), sticky="ew")

        ctk.CTkButton(form_frame, text="+ TAMBAH KAMAR", fg_color="#2ecc71", command=self.add_room).grid(row=2, column=0, columnspan=3, padx=15, pady=15, sticky="ew")

        # Table
        self.load_table()

    def load_table(self):
        # Hapus tabel lama jika ada
        if hasattr(self, 'list_container'): self.list_container.destroy()
        
        ctk.CTkLabel(self, text="List Kamar Terdaftar", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(10, 5))
        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(fill="x")

        header = ctk.CTkFrame(self.list_container, height=35, fg_color="gray25")
        header.pack(fill="x", pady=2)
        for t, w in [("No. Kamar", 100), ("Tipe", 200), ("Harga", 150), ("Status", 100), ("Aksi", 100)]:
             ctk.CTkLabel(header, text=t, width=w, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)

        rooms = logic.get_all_rooms()
        for r in rooms:
            row = ctk.CTkFrame(self.list_container, height=40, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=r[1], width=100).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=r[2], width=200).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"Rp {r[3]:,}", width=150).pack(side="left", padx=5)
            status_color = "#2ecc71" if r[4] == 'Available' else "#e74c3c"
            ctk.CTkLabel(row, text=r[4], text_color=status_color, width=100, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
            ctk.CTkButton(row, text="Hapus", width=80, height=25, fg_color="transparent", border_color="#e74c3c", border_width=1, text_color="#e74c3c", command=lambda id=r[0]: self.delete_room(id)).pack(side="left", padx=5)

    def add_room(self):
        try:
            logic.add_room(self.entry_no.get(), self.combo_type.get(), self.entry_price.get())
            messagebox.showinfo("Sukses", "Kamar ditambahkan!")
            self.load_table() # Refresh
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_room(self, room_id):
        if messagebox.askyesno("Konfirmasi", "Hapus kamar ini?"):
            logic.delete_room(room_id)
            self.load_table()