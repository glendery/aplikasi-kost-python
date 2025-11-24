import sqlite3

DB_NAME = "kost_management.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL, 
        price INTEGER NOT NULL,
        status TEXT DEFAULT 'Available'
    )''')
    
    # UPDATE: Tambah kolom payment_status
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        ktp_number TEXT,
        entry_date DATE NOT NULL,
        due_date_date INTEGER NOT NULL,
        payment_status TEXT DEFAULT 'Belum Bayar', 
        room_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES rooms (id)
    )''')
    conn.commit()
    conn.close()

# --- GET DATA FUNCTIONS ---
def get_dashboard_stats():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM rooms")
        total = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM rooms WHERE status='Occupied'")
        occupied = cur.fetchone()[0]
        conn.close()
        return {"total": total, "occupied": occupied, "available": total - occupied}
    except:
        return {"total": 0, "occupied": 0, "available": 0}

def get_all_rooms():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM rooms")
        data = cur.fetchall()
        conn.close()
        return data
    except:
        return []

def get_available_rooms():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT id, room_number, type FROM rooms WHERE status='Available'")
        data = cur.fetchall()
        conn.close()
        return data
    except:
        return []

# UPDATE: Fungsi Get Semua Tenant (Default)
def get_all_tenants():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        query = """
            SELECT t.id, t.full_name, t.phone_number, t.payment_status, t.due_date_date, t.room_id, r.room_number
            FROM tenants t
            JOIN rooms r ON t.room_id = r.id
        """
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        return data
    except:
        return []

# BARU: Fungsi SEARCH Tenant
def search_tenants(keyword):
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        # Cari berdasarkan Nama OR Nomor Kamar
        query = """
            SELECT t.id, t.full_name, t.phone_number, t.payment_status, t.due_date_date, t.room_id, r.room_number
            FROM tenants t
            JOIN rooms r ON t.room_id = r.id
            WHERE t.full_name LIKE ? OR r.room_number LIKE ?
        """
        # Tambahkan % di kiri kanan keyword untuk pencarian fleksibel
        search_term = f"%{keyword}%"
        cur.execute(query, (search_term, search_term))
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(e)
        return []

# --- ACTION FUNCTIONS ---
def add_room(number, r_type, price):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE room_number=?", (number,))
    if cur.fetchone():
        conn.close()
        raise ValueError(f"Kamar nomor {number} sudah ada!")
    cur.execute("INSERT INTO rooms (room_number, type, price, status) VALUES (?, ?, ?, 'Available')", 
                (number, r_type, int(price)))
    conn.commit()
    conn.close()

def delete_room(room_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM rooms WHERE id=?", (room_id,))
    conn.commit()
    conn.close()

# UPDATE: Tambah default status 'Belum Bayar'
def add_tenant(name, phone, due_date, room_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tenants (full_name, phone_number, ktp_number, entry_date, due_date_date, payment_status, room_id)
        VALUES (?, ?, ?, DATE('now'), ?, 'Belum Bayar', ?)
    """, (name, phone, "-", due_date, room_id))
    cur.execute("UPDATE rooms SET status='Occupied' WHERE id=?", (room_id,))
    conn.commit()
    conn.close()

# BARU: Update Status Pembayaran
def update_payment_status(tenant_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE tenants SET payment_status=? WHERE id=?", (new_status, tenant_id))
    conn.commit()
    conn.close()

def delete_room_by_number(room_number):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Hapus kamar berdasarkan nomornya
    cur.execute("DELETE FROM rooms WHERE room_number=?", (room_number,))
    conn.commit()
    conn.close()