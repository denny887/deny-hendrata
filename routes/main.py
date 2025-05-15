from flask import Blueprint, render_template
from models import PpdbSettings

main = Blueprint('main', __name__)

@main.route('/')
def index():
    settings = PpdbSettings.query.first()
    return render_template('index.html', settings=settings)
