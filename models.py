from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    asal_sekolah = db.Column(db.String(150), nullable=False)
    tempat_lahir = db.Column(db.String(150), nullable=False)
    nilai = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ijazah_file = db.Column(db.String(255))
    bukti_pembayaran = db.Column(db.String(255))
    rapor_file = db.Column(db.String(255))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
