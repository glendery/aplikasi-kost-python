import customtkinter as ctk
from tkinter import messagebox
from database import logic

class PaymentsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Header
        ctk.CTkLabel(self, text="Laporan & Monitoring Pembayaran", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0, 20))

        # --- SEARCH BAR ---
        search_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        search_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(search_frame, text="Cari Penghuni:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15, pady=10)
        
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Ketik Nama / No Kamar...", width=250)
        self.entry_search.pack(side="left", padx=5, pady=10)
        # Tekan Enter untuk cari
        self.entry_search.bind("<Return>", lambda event: self.search_action())

        btn_search = ctk.CTkButton(search_frame, text="🔍 Cari", width=80, fg_color="#4a90e2", command=self.search_action)
        btn_search.pack(side="left", padx=5, pady=10)
        
        btn_reset = ctk.CTkButton(search_frame, text="Reset", width=80, fg_color="gray", command=self.reset_search)
        btn_reset.pack(side="left", padx=5, pady=10)

        # --- TABEL PEMBAYARAN ---
        ctk.CTkLabel(self, text="Status Tagihan Bulan Ini", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(10, 5))
        
        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True)

        self.load_table()

    def load_table(self, data=None):
        # Bersihkan tabel lama
        for widget in self.list_container.winfo_children():
            widget.destroy()

        # Header Tabel
        header = ctk.CTkFrame(self.list_container, height=35, fg_color="gray25")
        header.pack(fill="x", pady=2)
        
        headers = [("Nama Penghuni", 200), ("Kamar", 80), ("Jatuh Tempo", 120), ("Status", 120), ("Aksi", 100)]
        for h_text, h_width in headers:
             ctk.CTkLabel(header, text=h_text, width=h_width, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)

        # Ambil Data
        if data is None:
            data = logic.get_all_tenants()

        if not data:
            ctk.CTkLabel(self.list_container, text="Data tidak ditemukan.").pack(pady=20)
            return

        for t in data:
            # t = (id, full_name, phone, payment_status, due_date, room_id, room_number)
            t_id = t[0]
            t_name = t[1]
            t_status = t[3]
            t_due = t[4]
            t_room_no = t[6]

            row = ctk.CTkFrame(self.list_container, height=45, fg_color="#2b2b2b")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=t_name, width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkButton(row, text=f"{t_room_no}", width=80, height=25, fg_color="#4a90e2", hover=False).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"Tgl {t_due}", width=120).pack(side="left", padx=5)

            # STATUS BADGE
            status_color = "#2ecc71" if t_status == "Lunas" else "#e74c3c"
            ctk.CTkLabel(row, text=t_status, text_color=status_color, width=120, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)

            # TOMBOL AKSI
            if t_status == "Belum Bayar":
                ctk.CTkButton(row, text="Bayar", width=100, height=25, fg_color="#2ecc71", 
                              command=lambda id=t_id: self.mark_as_paid(id)).pack(side="left", padx=5)
            else:
                ctk.CTkButton(row, text="Batal", width=100, height=25, fg_color="transparent", border_width=1, border_color="gray", text_color="gray",
                              command=lambda id=t_id: self.mark_as_unpaid(id)).pack(side="left", padx=5)

    def search_action(self):
        keyword = self.entry_search.get()
        if keyword:
            results = logic.search_tenants(keyword)
            self.load_table(results)
        else:
            self.load_table()

    def reset_search(self):
        self.entry_search.delete(0, 'end')
        self.load_table()

    def mark_as_paid(self, tenant_id):
        if messagebox.askyesno("Konfirmasi", "Tandai bulan ini sebagai SUDAH BAYAR (LUNAS)?"):
            logic.update_payment_status(tenant_id, "Lunas")
            self.search_action() # Refresh

    def mark_as_unpaid(self, tenant_id):
        if messagebox.askyesno("Konfirmasi", "Batalkan status lunas?"):
            logic.update_payment_status(tenant_id, "Belum Bayar")
            self.search_action()