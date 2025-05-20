from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db, Siswa, User, Chat, PpdbSettings

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Anda harus login sebagai admin.', 'error')
        return redirect(url_for('auth.admin_login'))
        
    # Calculate statistics
    total_pendaftar = Siswa.query.count()
    total_diterima = Siswa.query.filter_by(status='approved').count()
    total_pending = Siswa.query.filter_by(status='pending').count()
    total_ditolak = Siswa.query.filter_by(status='rejected').count()
    
    # Get all students data
    siswa_data = Siswa.query.all()
    
    return render_template('admin/dashboard.html',
                         total_pendaftar=total_pendaftar,
                         total_diterima=total_diterima,
                         total_pending=total_pending,
                         total_ditolak=total_ditolak,
                         siswa_data=siswa_data)

@admin.route('/approve/<int:siswa_id>')
def approve_siswa(siswa_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('auth.admin_login'))
        
    siswa = Siswa.query.get_or_404(siswa_id)
    siswa.status = 'approved'
    db.session.commit()
    flash('Siswa telah disetujui!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/reject/<int:siswa_id>')
def reject_siswa(siswa_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('auth.admin_login'))
        
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

@admin.route('/delete-rejected', methods=['POST'])
def delete_rejected():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('auth.admin_login'))
    
    try:
        rejected_students = Siswa.query.filter_by(status='rejected').all()
        for siswa in rejected_students:
            db.session.delete(siswa)
        db.session.commit()
        flash('Semua data siswa yang ditolak telah dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data siswa yang ditolak.', 'error')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete-users', methods=['POST'])
def delete_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('auth.admin_login'))
    
    try:
        # Get emails from the form
        emails_to_delete = request.form.get('emails').split(',')
        emails_to_delete = [email.strip() for email in emails_to_delete if email.strip()]
        
        if not emails_to_delete:
            flash('Tidak ada email yang diberikan untuk dihapus.', 'error')
            return redirect(url_for('admin.dashboard'))
        
        users_to_delete = User.query.filter(User.username.in_(emails_to_delete)).all()
        
        for user in users_to_delete:
            # Delete associated student data if exists
            Siswa.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
        
        db.session.commit()
        flash('Data pengguna berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data pengguna.', 'error')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('admin.dashboard'))

@admin.route('/announcement-settings', methods=['GET', 'POST'])
def announcement_settings():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak!', 'error')
        return redirect(url_for('auth.admin_login'))
        
    settings = PpdbSettings.query.first()
    if request.method == 'POST':
        if not settings:
            settings = PpdbSettings()
            db.session.add(settings)
            
        settings.announcement_title = request.form.get('announcement_title')
        settings.announcement_content = request.form.get('announcement_content')
        settings.show_announcement = request.form.get('show_announcement') == 'on'
        
        try:
            db.session.commit()
            flash('Pengaturan pengumuman berhasil diperbarui!', 'success')
        except:
            db.session.rollback()
            flash('Gagal memperbarui pengaturan pengumuman!', 'error')
            
    return render_template('admin/announcement_settings.html', settings=settings)

def is_admin():
    return 'user_id' in session and session.get('role') == 'admin'
