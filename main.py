import customtkinter as ctk
from database import logic

# --- IMPORT VIEWS (Pastikan file-file ini ada di folder views/) ---
from views.dashboard_view import DashboardView
from views.rooms_view import RoomsView
from views.tenants_view import TenantsView
from views.payments_view import PaymentsView  # <--- IMPORT BARU

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class KostApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KOST ELITE - Owner Dashboard System")
        self.geometry("1200x700")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Jalankan Database Init (Membuat tabel baru jika belum ada)
        logic.init_db()

        # 2. Setup UI Dasar
        self.setup_sidebar()
        self.main_content = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # 3. Buka Dashboard Awal
        self.show_view("Dashboard")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Logo
        ctk.CTkLabel(self.sidebar_frame, text="KOST ELITE\nManagement", 
                     font=ctk.CTkFont(size=22, weight="bold"), 
                     text_color="#4a90e2").grid(row=0, column=0, padx=20, pady=(30, 20))

        # --- TOMBOL NAVIGASI ---
        self.create_btn("Dashboard", lambda: self.show_view("Dashboard"), 1)
        self.create_btn("Data Kamar", lambda: self.show_view("Rooms"), 2)
        self.create_btn("Data Penghuni", lambda: self.show_view("Tenants"), 3)
        self.create_btn("Laporan Keuangan", lambda: self.show_view("Payments"), 4) # <--- TOMBOL BARU
        
        # Versi App
        ctk.CTkLabel(self.sidebar_frame, text="v1.1.0 Pro", text_color="gray").grid(row=6, column=0, pady=20)

    def create_btn(self, text, cmd, row):
        ctk.CTkButton(self.sidebar_frame, text=text, command=cmd, 
                      height=40, corner_radius=8, 
                      fg_color="transparent", hover_color="#3a3a3a", 
                      anchor="w", font=ctk.CTkFont(size=14)).grid(row=row, column=0, padx=15, pady=5, sticky="ew")

    # --- FUNGSI NAVIGASI PINTAR ---
    def show_view(self, view_name):
        # 1. Bersihkan area konten (hapus tampilan lama)
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # 2. Tampilkan tampilan baru sesuai tombol yang ditekan
        if view_name == "Dashboard":
            DashboardView(self.main_content, self).pack(fill="both", expand=True)
        elif view_name == "Rooms":
            RoomsView(self.main_content, self).pack(fill="both", expand=True)
        elif view_name == "Tenants":
            TenantsView(self.main_content, self).pack(fill="both", expand=True)
        elif view_name == "Payments":  # <--- LOGIKA BARU
            PaymentsView(self.main_content, self).pack(fill="both", expand=True)

if __name__ == "__main__":
    app = KostApp()
    app.mainloop()