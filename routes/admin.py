from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db, Siswa, User, Chat, PpdbSettings

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Anda harus login sebagai admin.', 'error')
        return redirect(url_for('auth.login'))
        
    # Get all students data including pending, approved, and rejected
    siswa_data = Siswa.query.order_by(Siswa.id.desc()).all()
    # Get all users for chat functionality
    users = User.query.filter_by(role='user').all()
    
    return render_template('admin/dashboard.html', 
                         siswa_data=siswa_data,
                         users=users)

@admin.route('/approve/<int:siswa_id>')
def approve_siswa(siswa_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('login'))
        
    siswa = Siswa.query.get_or_404(siswa_id)
    siswa.status = 'approved'
    db.session.commit()
    flash('Siswa telah disetujui!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/reject/<int:siswa_id>')
def reject_siswa(siswa_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('login'))
        
    siswa = Siswa.query.get_or_404(siswa_id)
    siswa.status = 'rejected'
    db.session.commit()
    flash('Siswa telah ditolak!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete/<int:siswa_id>')
def delete_siswa(siswa_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('login'))
    
    siswa = Siswa.query.get_or_404(siswa_id)
    db.session.delete(siswa)
    db.session.commit()
    flash('Data siswa telah dihapus!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/chat/<int:user_id>')
def chat(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('login'))
        
    users = User.query.filter_by(role='user').all()
    chats = Chat.query.filter_by(user_id=user_id).order_by(Chat.timestamp).all()
    
    return render_template('admin/dashboard.html', 
                         users=users, 
                         chats=chats, 
                         selected_user=user_id)

@admin.route('/send-message/<int:user_id>', methods=['POST'])
def send_message(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('login'))
        
    message = request.form.get('message')
    if message:
        chat = Chat(
            user_id=user_id,
            message=message,
            is_admin=True
        )
        db.session.add(chat)
        db.session.commit()
        
    return redirect(url_for('admin.chat', user_id=user_id))

@admin.route('/settings', methods=['GET', 'POST'])
def settings():
    if not is_admin():
        return redirect(url_for('login'))
        
    settings = PpdbSettings.query.first()
    if request.method == 'POST':
        try:
            if not settings:
                settings = PpdbSettings()
                db.session.add(settings)
                
            settings.registration_open = request.form.get('registration_status') == 'open'
            settings.academic_year = request.form.get('academic_year')
            settings.quota_per_major = request.form.get('quota_per_major', type=int)
            settings.announcement_title = request.form.get('announcement_title')
            settings.announcement_content = request.form.get('announcement_content')
            settings.show_announcement = request.form.get('show_announcement') == 'show'
            
            db.session.commit()
            flash('Pengaturan berhasil diperbarui', 'success')
        except:
            db.session.rollback()
            flash('Gagal memperbarui pengaturan', 'error')
            
    return render_template('admin/settings.html', settings=settings)

def is_admin():
    return 'user_id' in session and session.get('role') == 'admin'
