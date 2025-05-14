import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Siswa
import re
from routes.admin import admin
from routes.user import user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add this line for session management

# Add these lines after app creation and before database setup
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# After app creation, add these configurations
app.static_folder = 'static'
app.static_url_path = '/static'

# Create database directory if it doesn't exist
db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
os.makedirs(db_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_dir, "ppdb.db")}'

# Modify the database connection handling
try:
    db.init_app(app)
except Exception as e:
    print(f"Database connection error: {e}")

# Add these configurations after app creation
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create required directories
STATIC_FOLDERS = [
    os.path.join(app.static_folder, 'uploads'),
    os.path.join(app.static_folder, 'programs'),
    os.path.join(app.static_folder, 'achievements'),
    os.path.join(app.static_folder, 'icons')
]

for folder in STATIC_FOLDERS:
    os.makedirs(folder, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add static file helper function
def verify_static_files():
    required_images = {
        'programs': ['RPL.jpg', 'HOTEL.jpg', 'BENGKEL.jpg'],
        'achievements': ['campus.jpg', 'lab.jpg', 'industry.jpg'],
        'icons': ['instagram.png', 'MAP.png'],
        '.': ['logo.png']  # Check in root static folder
    }
    
    missing_files = []
    for folder, files in required_images.items():
        folder_path = os.path.join(app.static_folder, folder)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                missing_files.append(f"{folder}/{file}")
    
    if missing_files:
        print("Warning: Missing static files:", missing_files)

# Register blueprints
app.register_blueprint(admin)
app.register_blueprint(user)

# Keep only general routes in app.py
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"Admin login attempt - username: {username}")  # Debug print
        
        admin = User.query.filter_by(username=username, role='admin').first()
        if admin and password == 'admin123':  # Direct password comparison for admin
            session['user_id'] = admin.id
            session['role'] = 'admin'
            print("Admin login successful")  # Debug print
            return redirect(url_for('admin.dashboard'))
            
        flash('Username atau password admin salah!', 'error')
        print("Admin login failed")  # Debug print
    return render_template('admin/login.html')

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
    return render_template('user/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate email format
        if not username.endswith(('@gmail.com', '@yahoo.com', '@hotmail.com')):
            flash('Email harus menggunakan domain @gmail.com, @yahoo.com, atau @hotmail.com', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Email sudah terdaftar!', 'error')
            return render_template('register.html')
            
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role='user')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Pendaftaran berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Add basic logging
@app.before_request
def before_request():
    print(f"Incoming {request.method} request to {request.path}")

# Modify the main run section at the bottom
if __name__ == '__main__':
    try:
        with app.app_context():
            # Delete existing database file
            db_file = os.path.join(db_dir, "ppdb.db")
            if os.path.exists(db_file):
                os.remove(db_file)
                print("Existing database deleted")
            
            # Create new tables
            db.create_all()
            print("New database tables created")
            
            # Create admin account
            admin = User(
                username='admin@admin.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin account created successfully")
            
            verify_static_files()
        
        app.run(
            host='127.0.0.1',  # Changed from 0.0.0.0 to 127.0.0.1
            port=5000,
            debug=True
        )
    except Exception as e:
        print(f"Server startup error: {e}")
        raise e  # Add this to see full error traceback
