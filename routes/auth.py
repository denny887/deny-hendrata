from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.role == 'user' and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('user.dashboard'))
        else:
            flash('Username atau password salah!', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = User.query.filter_by(username=username, role='admin').first()
        if admin and password == 'admin123':
            session['user_id'] = admin.id
            session['role'] = 'admin'
            return redirect(url_for('admin.dashboard'))
            
        flash('Username atau password admin salah!', 'error')
    return render_template('auth/admin_login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username.endswith(('@gmail.com', '@yahoo.com', '@hotmail.com')):
            flash('Email harus menggunakan domain @gmail.com, @yahoo.com, atau @hotmail.com', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Email sudah terdaftar!', 'error')
            return render_template('auth/register.html')
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role='user')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Pendaftaran berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
