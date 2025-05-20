# Jalankan file ini dengan: python add_jurusan_column.py
# Ini akan menambah kolom jurusan ke tabel siswa jika belum ada.
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'ppdb.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE siswa ADD COLUMN jurusan VARCHAR(100);")
    print("Kolom 'jurusan' berhasil ditambahkan ke tabel 'siswa'.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e) or "already exists" in str(e):
        print("Kolom 'jurusan' sudah ada.")
    else:
        print("Error:", e)
finally:
    conn.commit()
    conn.close()