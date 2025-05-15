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
            # Validate input
            nama = request.form.get('nama')
            if not re.match(r'^[a-zA-Z\s]{3,50}$', nama):
                flash('Nama tidak valid', 'error')
                return redirect(url_for('user.dashboard'))
                
            files = {'ijazah': request.files.get('ijazah'),
                    'bukti_pembayaran': request.files.get('bukti_pembayaran'),
                    'rapor': request.files.get('rapor')}
            
            file_paths = {}
            for file_type, file in files.items():
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{session['user_id']}_{file_type}_{file.filename}")
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    file_paths[f"{file_type}_file"] = filename
                else:
                    flash(f'File {file_type} tidak valid', 'error')
                    return redirect(url_for('user.dashboard'))

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
            flash('Data berhasil disimpan', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan, silakan coba lagi', 'error')
            print(f"Error: {str(e)}")
        
    siswa_data = Siswa.query.filter_by(user_id=session['user_id']).all()
    chats = Chat.query.filter_by(user_id=session['user_id']).order_by(Chat.timestamp).all()
    
    return render_template('user/dashboard.html', siswa_data=siswa_data, chats=chats)

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
