from flask import Blueprint, render_template
from models import PpdbSettings, Siswa

main = Blueprint('main', __name__)

@main.route('/')
def index():
    settings = PpdbSettings.query.first()
    return render_template('index.html', settings=settings)

@main.route('/alur')
def alur():
    return render_template('alur.html')

@main.route('/pengumuman')
def pengumuman():
    settings = PpdbSettings.query.first()
    approved_students = Siswa.query.filter_by(status='approved').all()
    return render_template('pengumuman.html', 
                         settings=settings,
                         approved_students=approved_students)

@main.route('/alur-pendaftaran')
def alur_pendaftaran():
    return render_template('alur_pendaftaran.html')
