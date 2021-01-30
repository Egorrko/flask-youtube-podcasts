from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import youtube
import config
import os.path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_ADDRESS

db = SQLAlchemy(app)

from models import *

if not os.path.exists(config.DATABASE_PATH):
    db.create_all()


@app.route('/')
def index():
    podcasts = youtube.get()
    return render_template('podcasts.html', podcasts=podcasts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    link = None
    result = None
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        result = youtube.download(link)
        if result:
            return redirect('/')
        else:
            result = 'Ошибка загрузки. Проверьте ссылку'
    return render_template('add.html', error=result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form['login']
    password = request.form['password']
    if login and password:
        User.create(User(login, password))
    print(User.query.all())
    return redirect('/')
