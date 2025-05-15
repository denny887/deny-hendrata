from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db, Siswa, User, Chat, SchoolSettings, PpdbSettings, Major

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Anda harus login sebagai admin.', 'error')
        return redirect(url_for('login'))
        
    siswa_data = Siswa.query.all()
    return render_template('admin/dashboard.html', siswa_data=siswa_data)

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

@admin.route('/settings', methods=['GET'])
def settings():
    if not is_admin():
        return redirect(url_for('login'))
    settings = PpdbSettings.query.first()
    majors = Major.query.filter_by(active=True).all()
    return render_template('admin/settings.html', settings=settings, majors=majors)

@admin.route('/update-settings', methods=['POST'])
def update_settings():
    if not is_admin():
        return redirect(url_for('login'))
        
    settings = PpdbSettings.query.first()
    if not settings:
        settings = PpdbSettings()
        db.session.add(settings)
        
    settings.registration_open = request.form.get('registration_status') == 'open'
    settings.academic_year = request.form.get('academic_year')
    settings.quota_per_major = request.form.get('quota_per_major', type=int)
    
    db.session.commit()
    flash('Pengaturan berhasil diperbarui', 'success')
    return redirect(url_for('admin.settings'))

@admin.route('/update-majors', methods=['POST'])
def update_majors():
    if not is_admin():
        return redirect(url_for('login'))
        
    major_names = request.form.getlist('major_name[]')
    major_quotas = request.form.getlist('major_quota[]')
    
    # Deactivate all existing majors
    Major.query.update({Major.active: False})
    
    # Add or update majors
    for name, quota in zip(major_names, major_quotas):
        if name:
            major = Major.query.filter_by(name=name).first()
            if not major:
                major = Major(name=name)
            major.quota = int(quota)
            major.active = True
            db.session.add(major)
            
    db.session.commit()
    flash('Program keahlian berhasil diperbarui', 'success')
    return redirect(url_for('admin.settings'))

@admin.route('/update-announcement', methods=['POST'])
def update_announcement():
    if not is_admin():
        return redirect(url_for('login'))
        
    settings = PpdbSettings.query.first()
    if not settings:
        settings = PpdbSettings()
        db.session.add(settings)
        
    settings.announcement_title = request.form.get('announcement_title')
    settings.announcement_content = request.form.get('announcement_content')
    settings.show_announcement = request.form.get('announcement_status') == 'show'
    
    db.session.commit()
    flash('Pengumuman berhasil diperbarui', 'success')
    return redirect(url_for('admin.settings'))

def is_admin():
    return 'user_id' in session and session.get('role') == 'admin'
