import customtkinter as ctk
from database import logic

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Header
        ctk.CTkLabel(self, text="Dashboard Overview", font=ctk.CTkFont(size=28, weight="bold"), anchor="w").pack(fill="x", pady=(0, 20))

        # Stats Cards
        stats_container = ctk.CTkFrame(self, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 30))
        
        stats = logic.get_dashboard_stats()
        
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        stats_container.grid_columnconfigure(2, weight=1)

        self.create_stat_card(stats_container, "Total Kamar", str(stats['total']), "#4a90e2", 0)
        self.create_stat_card(stats_container, "Kamar Terisi", str(stats['occupied']), "#e74c3c", 1)
        self.create_stat_card(stats_container, "Kamar Kosong", str(stats['available']), "#2ecc71", 2)

        # Room Status Visual
        ctk.CTkLabel(self, text="Status Kamar Real-time", font=ctk.CTkFont(size=20, weight="bold"), anchor="w").pack(fill="x", pady=(10, 15))
        rooms_container = ctk.CTkFrame(self, fg_color="transparent")
        rooms_container.pack(fill="x")

        rooms = logic.get_all_rooms()
        row, col = 0, 0
        for room in rooms:
            r_num, r_type, r_status = room[1], room[2], room[4]
            bg_color = "#2ecc71" if r_status == 'Available' else "#e74c3c"
            status_text = "KOSONG" if r_status == 'Available' else "TERISI"

            card = ctk.CTkFrame(rooms_container, width=150, height=100, corner_radius=10, fg_color="#2b2b2b")
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=f"No. {r_num}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10,0))
            ctk.CTkLabel(card, text=r_type, font=ctk.CTkFont(size=12)).pack()
            ctk.CTkButton(card, text=status_text, fg_color=bg_color, hover=False, height=25, width=80, corner_radius=20).pack(pady=(10, 10))

            col += 1
            if col > 3: 
                col = 0
                row += 1

    def create_stat_card(self, parent, title, value, color, col_idx):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="#2b2b2b", border_width=2, border_color=color)
        card.grid(row=0, column=col_idx, padx=10, sticky="ew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color="gray").pack(pady=(15, 5))
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=36, weight="bold"), text_color=color).pack(pady=(0, 15))