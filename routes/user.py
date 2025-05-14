from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models import db, Siswa, Chat
import os

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        # Handle file uploads and form submission
        # ...existing file upload code...
        pass  # Placeholder to avoid indentation error
        
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
