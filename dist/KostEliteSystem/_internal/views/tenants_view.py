import customtkinter as ctk
from tkinter import messagebox
from database import logic

class TenantsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        ctk.CTkLabel(self, text="Check-In Penghuni", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # Form
        input_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        input_frame.pack(fill="x", pady=(0, 20))
        input_frame.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(input_frame, text="Nama Lengkap:").grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(input_frame)
        self.entry_name.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="No. Handphone:").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.entry_phone = ctk.CTkEntry(input_frame)
        self.entry_phone.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        ctk.CTkLabel(input_frame, text="Pilih Kamar:").grid(row=0, column=1, padx=20, pady=5, sticky="w")
        self.combo_rooms = ctk.CTkOptionMenu(input_frame, values=[])
        self.combo_rooms.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(input_frame, text="Tgl Tagihan (1-31):").grid(row=2, column=1, padx=20, pady=5, sticky="w")
        self.entry_due = ctk.CTkEntry(input_frame)
        self.entry_due.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="ew")

        ctk.CTkButton(input_frame, text="SIMPAN PENGHUNI", fg_color="#4a90e2", command=self.save_tenant).grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.refresh_room_options()
        self.load_table()

    def refresh_room_options(self):
        rooms = logic.get_available_rooms()
        self.room_options = [f"Kamar {r[1]} - {r[2]}" for r in rooms]
        self.room_ids = [r[0] for r in rooms]
        self.combo_rooms.configure(values=self.room_options if self.room_options else ["Penuh"])

    def load_table(self):
        if hasattr(self, 'list_container'): self.list_container.destroy()
        
        ctk.CTkLabel(self, text="Daftar Penghuni Aktif", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(10, 10))
        self.list_container = ctk.CTkFrame(self, fg_color="transparent")
        self.list_container.pack(fill="x")

        header = ctk.CTkFrame(self.list_container, height=30, fg_color="gray20")
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="Nama", width=200, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header, text="Kamar", width=100).pack(side="left", padx=10)
        ctk.CTkLabel(header, text="No. HP", width=150, anchor="w").pack(side="left", padx=10)

        tenants = logic.get_all_tenants()
        for t in tenants:
            row = ctk.CTkFrame(self.list_container, height=40, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=t[1], width=200, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            ctk.CTkButton(row, text=f"{t[7]}", width=100, height=25, fg_color="#4a90e2", hover=False).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=t[2], width=150, anchor="w").pack(side="left", padx=10)

    def save_tenant(self):
        try:
            idx = self.room_options.index(self.combo_rooms.get())
            logic.add_tenant(self.entry_name.get(), self.entry_phone.get(), self.entry_due.get(), self.room_ids[idx])
            messagebox.showinfo("Sukses", "Check-in Berhasil!")
            self.refresh_room_options()
            self.load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal: {e}")