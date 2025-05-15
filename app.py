import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Siswa
import re
from routes.admin import admin
from routes.user import user
from routes.auth import auth
from routes.main import main

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
app.register_blueprint(auth)
app.register_blueprint(main)

# Remove the routes that were moved to blueprints

# Add basic logging
@app.before_request
def before_request():
    print(f"Incoming {request.method} request to {request.path}")

def create_tables():
    with app.app_context():
        db.create_all()
        # Create initial PPDB settings if not exists
        from models import PpdbSettings
        if not PpdbSettings.query.first():
            initial_settings = PpdbSettings(
                registration_open=True,
                academic_year="2024/2025",
                quota_per_major=40,
                announcement_title="Pengumuman PPDB",
                announcement_content="Selamat datang di PPDB SMK Karya Bangsa",
                show_announcement=True
            )
            db.session.add(initial_settings)
            db.session.commit()

# Modify the main run section at the bottom
if __name__ == '__main__':
    create_tables()
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
