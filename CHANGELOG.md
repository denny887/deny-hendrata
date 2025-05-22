# CHANGELOG

## v1.0.0 - 2024-05-22

### Fitur Baru
- Penambahan fitur upload Fast Foto (pas foto) pada dashboard siswa.
- Penambahan fitur chat antara siswa dan admin di dashboard siswa dan admin.
- Penambahan pengaturan pengumuman oleh admin.
- Penambahan pengaturan QRIS pembayaran dan biaya pendaftaran oleh admin.
- Penambahan pengaturan jurusan dan kuota oleh admin.
- Penambahan penghapusan user berdasarkan email oleh admin.
- Penambahan log aktivitas sistem untuk admin.

### Perbaikan & Peningkatan
- Perbaikan tampilan gambar (testimoni, program, dsb) agar kepala tidak terpotong, dengan pengaturan ukuran dan object-fit.
- Penambahan field jenis kelamin pada form pendaftaran dan tampilan data siswa.
- Perbaikan label status pendaftar di dashboard admin menjadi bahasa Indonesia: Diterima, Ditolak, Menunggu.
- Penambahan link ke website sekolah Karya Bangsa lain (SMK, SMP, SD) di halaman utama dan dashboard siswa.
- Penambahan validasi file upload (ukuran maksimal 5MB).
- Penambahan tampilan progress pendaftaran di dashboard siswa.
- Penambahan tampilan pengumuman hasil seleksi di halaman pengumuman.

### Struktur & Organisasi
- Penambahan struktur folder: static/uploads, static/programs, static/achievements, static/icons.
- Penambahan script add_jurusan_column.py untuk migrasi kolom jurusan.
- Penambahan model Major dan Registration pada models.py.
- Refactor routes menjadi blueprint: main, user, admin, auth.

### Lain-lain
- Penambahan dokumentasi README beserta penjelasan setiap cuplikan layar.
- Penambahan requirements.txt dan instruksi instalasi.
- Penambahan WhatsApp floating button di seluruh halaman.

---
