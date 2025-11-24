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
    cur.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        ktp_number TEXT,
        entry_date DATE NOT NULL,
        due_date_date INTEGER NOT NULL,
        room_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES rooms (id)
    )''')
    conn.commit()
    conn.close()

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

def add_room(number, r_type, price):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM rooms WHERE room_number=?", (number,))
    if cur.fetchone():
        conn.close()
        raise Exception(f"Kamar nomor {number} sudah ada!")
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

def get_available_rooms():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, room_number, type FROM rooms WHERE status='Available'")
    data = cur.fetchall()
    conn.close()
    return data

def add_tenant(name, phone, due_date, room_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO tenants (full_name, phone_number, ktp_number, entry_date, due_date_date, room_id)
        VALUES (?, ?, ?, DATE('now'), ?, ?)
    """, (name, phone, "-", due_date, room_id))
    cur.execute("UPDATE rooms SET status='Occupied' WHERE id=?", (room_id,))
    conn.commit()
    conn.close()

def get_all_tenants():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = """
        SELECT t.id, t.full_name, t.phone_number, t.ktp_number, t.entry_date, t.due_date_date, t.room_id, r.room_number
        FROM tenants t
        JOIN rooms r ON t.room_id = r.id
    """
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return data