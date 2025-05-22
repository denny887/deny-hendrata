

## Struktur Proyek

![Cuplikan Layar](static/images/Cuplikan%20layar%202025-05-22%20111917.png)
![Cuplikan Layar 2](static/images/Cuplikan%20layar%202025-05-22%20114202.png)
![Cuplikan Layar 3](static/images/Cuplikan%20layar%202025-05-22%20111957.png)
![Cuplikan Layar 4](static/images/Cuplikan%20layar%202025-05-22%20111950.png)
![Cuplikan Layar 5](static/images/Cuplikan%20layar%202025-05-22%20111940.png)
![Cuplikan Layar 6](static/images/Cuplikan%20layar%202025-05-22%20114230.png)
![Cuplikan Layar 7](static/images/Cuplikan%20layar%202025-05-22%20114239.png)
![Cuplikan Layar 8](static/images/Cuplikan%20layar%202025-05-22%20114302.png)
![Cuplikan Layar 9](static/images/Cuplikan%20layar%202025-05-22%20114310.png)
![Cuplikan Layar 10](static/images/Cuplikan%20layar%202025-05-22%20114319.png)
![Cuplikan Layar 11](static/images/Cuplikan%20layar%202025-05-22%20114328.png)
![Cuplikan Layar 12](static/images/Cuplikan%20layar%202025-05-22%20114352.png)
![Cuplikan Layar 13](static/images/Cuplikan%20layar%202025-05-22%20114406.png)
![Cuplikan Layar 14](static/images/Cuplikan%20layar%202025-05-22%20114413.png)
![Cuplikan Layar 15](static/images/Cuplikan%20layar%202025-05-22%20114423.png)
![Cuplikan Layar 16](static/images/Cuplikan%20layar%202025-05-22%20114443.png)
![Cuplikan Layar 17](static/images/Cuplikan%20layar%202025-05-22%20114454.png)
![Cuplikan Layar 18](static/images/Cuplikan%20layar%202025-05-22%20111940.png)

### Penjelasan Setiap Cuplikan Layar

1. **Cuplikan Layar 1**: Tampilan halaman beranda utama website PPDB SMK Karya Bangsa, menampilkan banner, tombol daftar, dan informasi utama.
2. **Cuplikan Layar 2**: Tampilan jadwal pendaftaran dan informasi penting PPDB pada halaman utama.
3. **Cuplikan Layar 3**: Tampilan fitur program keahlian/jurusan unggulan yang tersedia di SMK Karya Bangsa.
4. **Cuplikan Layar 4**: Tampilan testimoni alumni dan orang tua siswa di halaman utama.
5. **Cuplikan Layar 5**: Tampilan dashboard siswa setelah login, menampilkan status pendaftaran, data diri, upload dokumen, dan fitur chat dengan admin.
6. **Cuplikan Layar 6**: Tampilan halaman pengumuman hasil seleksi PPDB, menampilkan pengumuman resmi, jadwal, dan daftar siswa diterima.
7. **Cuplikan Layar 7**: Tampilan halaman admin dashboard, menampilkan statistik pendaftar, data siswa, dan fitur verifikasi.
8. **Cuplikan Layar 8**: Tampilan halaman admin untuk pengaturan pengumuman PPDB.
9. **Cuplikan Layar 9**: Tampilan halaman admin untuk menghapus pengguna berdasarkan email.
10. **Cuplikan Layar 10**: Tampilan halaman admin untuk pengaturan QRIS pembayaran PPDB.
11. **Cuplikan Layar 11**: Tampilan halaman admin untuk mengatur data jurusan (major), menambah/edit/hapus jurusan dan kuota.
12. **Cuplikan Layar 12**: Tampilan halaman admin untuk pengaturan data sekolah, status pendaftaran, tahun ajaran, kuota, dan QRIS.
13. **Cuplikan Layar 13**: Tampilan halaman admin untuk mengatur data jurusan secara detail, termasuk status aktif dan kuota.
14. **Cuplikan Layar 14**: Tampilan halaman admin untuk melihat dan mengelola data siswa yang sudah mendaftar.
15. **Cuplikan Layar 15**: Tampilan halaman admin untuk mengelola data chat antara admin dan siswa.
16. **Cuplikan Layar 16**: Tampilan halaman admin untuk mengelola data jurusan secara detail dan menampilkan statistik pendaftar per jurusan.
17. **Cuplikan Layar 17**: Tampilan halaman admin untuk melihat log aktivitas sistem atau riwayat aksi penting.
18. **Cuplikan Layar 18**: Tampilan dashboard siswa setelah login, menampilkan status pendaftaran, data diri, upload dokumen, dan fitur chat dengan admin.


Deskripsi singkat:
Website ini digunakan untuk proses Penerimaan Peserta Didik Baru (PPDB) secara online di SMK Karya Bangsa.

**Fitur utama:**
- Registrasi dan login siswa
- Formulir pendaftaran online
- Upload dokumen (ijazah, rapor, bukti pembayaran)
- Dashboard siswa & admin
- Pengumuman hasil seleksi
- Chat admin-siswa
- Pengaturan pengumuman oleh admin

**Teknologi:**  
Flask, SQLite, Bootstrap, FontAwesome, Google Fonts

**Cara menjalankan:**
1. Install requirements:  
   `pip install -r requirements.txt`
2. Jalankan aplikasi:  
   `python app.py`
3. Buka browser ke `http://127.0.0.1:5000`

---


## Penjelasan Struktur

- **app.py**: Entry point aplikasi Flask, inisialisasi app, konfigurasi, dan register blueprint.
- **models.py**: Definisi model database (User, Siswa, Chat, PpdbSettings, dsb) menggunakan SQLAlchemy.
- **requirements.txt**: Daftar dependensi Python.
- **add_jurusan_column.py**: Script untuk menambah kolom jurusan pada tabel siswa jika belum ada.
- **database/**: Folder database SQLite.
- **static/**: Folder untuk file statis (CSS, gambar, uploads, dsb).
- **templates/**: Folder template HTML (menggunakan Jinja2).
- **routes/**: Folder blueprint Flask untuk pemisahan route (main, user, admin, auth).

## Fitur Utama

- Registrasi dan login siswa serta admin
- Formulir pendaftaran online (dengan upload dokumen: ijazah, rapor, bukti pembayaran)
- Dashboard siswa (lihat status, data diri, chat admin)
- Dashboard admin (verifikasi, hapus, chat siswa, pengumuman, pengaturan sekolah)
- Pengumuman hasil seleksi dan jadwal PPDB
- Pengaturan jurusan, kuota, QRIS, dan pengumuman oleh admin
- Chat antara siswa dan admin

## Model Database

- **User**: Data user (siswa/admin), username, password, role
- **Siswa**: Data pendaftar (nama, asal sekolah, tempat lahir, nilai, jurusan, status, file upload, user_id)
- **Chat**: Pesan antara siswa dan admin
- **PpdbSettings**: Pengaturan PPDB (status pendaftaran, tahun ajaran, kuota, pengumuman)
- **Major**: Data jurusan dan kuota
- **Registration**: Relasi pendaftaran siswa ke jurusan

## Cara Menjalankan

1. Install requirements:  
   `pip install -r requirements.txt`
2. Jalankan aplikasi:  
   `python app.py`
3. Buka browser ke `http://127.0.0.1:5000`

---
ppdb-karsa/
├── app.py
├── models.py
├── add_jurusan_column.py
├── requirements.txt
├── database/
│   └── ppdb.db
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── user.py
│   ├── admin.py
│   └── auth.py
├── static/
│   ├── style.css
│   ├── images/
│   │   ├── LOGO_KARSA.png
│   │   ├── gedung_baru.jpg
│   │   ├── qris-dinncafe.png
│   │   └── ... (gambar lain & screenshot)
│   ├── uploads/
│   ├── programs/
│   ├── achievements/
│   └── icons/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── alur.html
│   ├── pengumuman.html
│   ├── login.html          # fallback atau general login
│   ├── register.html       # fallback atau general register
│   ├── user/
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── settings.html
│   │   ├── school_settings.html
│   │   └── announcement_settings.html
│   └── auth/
│       ├── login.html
│       ├── admin_login.html
│       └── register.html
