from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app
from models import db, Siswa, Chat
from werkzeug.utils import secure_filename
import os
import re

user = Blueprint('user', __name__, url_prefix='/user')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'jpg', 'jpeg', 'png'}

@user.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        try:
            # Validasi input
            nama = request.form.get('nama')
            if not re.match(r'^[a-zA-Z\s]{3,50}$', nama):
                flash('Nama tidak valid. Harus berupa huruf dan panjang 3-50 karakter.', 'error')
                return redirect(url_for('user.dashboard'))
                
            files = {
                'ijazah_file': request.files.get('ijazah'),
                'bukti_pembayaran': request.files.get('bukti_pembayaran'),
                'rapor_file': request.files.get('rapor')
            }
            
            file_paths = {}
            for field, file in files.items():
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{session['user_id']}_{field}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    try:
                        file.save(filepath)
                        file_paths[field] = filename
                    except Exception as e:
                        flash(f"Gagal menyimpan file {field}: {str(e)}", 'error')
                        print(f"Error saat menyimpan file {field}: {str(e)}")
                        return redirect(url_for('user.dashboard'))
                elif not file:
                    flash(f"File {field.replace('_file','').replace('_',' ').title()} wajib diunggah.", 'error')
                    return redirect(url_for('user.dashboard'))

            siswa = Siswa.query.filter_by(user_id=session['user_id']).first()
            if siswa:
                # Perbarui data yang sudah ada
                siswa.nama = nama
                siswa.asal_sekolah = request.form.get('asal_sekolah')
                siswa.tempat_lahir = request.form.get('tempat_lahir')
                siswa.nilai = int(request.form.get('nilai'))
                for key, value in file_paths.items():
                    setattr(siswa, key, value)
            else:
                # Buat data baru
                siswa = Siswa(
                    nama=nama,
                    asal_sekolah=request.form.get('asal_sekolah'),
                    tempat_lahir=request.form.get('tempat_lahir'),
                    nilai=int(request.form.get('nilai')),
                    user_id=session['user_id'],
                    **file_paths
                )
                db.session.add(siswa)
            db.session.commit()
            flash('Data berhasil disimpan.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat menyimpan data. Silakan coba lagi.', 'error')
            print(f"Error: {str(e)}")
        
    siswa = Siswa.query.filter_by(user_id=session['user_id']).first()
    
    # Calculate progress and status
    progress = 0
    status_text = "Belum Mendaftar"
    uploaded_files = 0
    
    if siswa:
        if siswa.ijazah_file:
            uploaded_files += 1
        if siswa.rapor_file:
            uploaded_files += 1
        if siswa.bukti_pembayaran:
            uploaded_files += 1
            
        if siswa.status == 'approved':
            progress = 100
            status_text = "Diterima"
        elif siswa.bukti_pembayaran:
            progress = 60
            status_text = "Menunggu Verifikasi"
        else:
            progress = 20
            status_text = "Melengkapi Berkas"
    
    return render_template('user/dashboard.html',
                         siswa=siswa,
                         progress=progress,
                         status_text=status_text,
                         uploaded_files=uploaded_files)

@user.route('/send-message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('login'))
        
    message = request.form.get('message')
    if message:
        chat = Chat(
            user_id=session['user_id'],
            message=message,
            is_admin=False
        )
        db.session.add(chat)
        db.session.commit()
        
    return redirect(url_for('user.dashboard'))
