from flask import Flask, render_template, current_app
from app import db
from app.models import User
from app.main import bp

@bp.route('/')
def index():
    title = "Home"
    return render_template('index.html', title=title)
