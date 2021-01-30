"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect
from YoutubePodcasts import app, youtube
from YoutubePodcasts.models import Users
from YoutubePodcasts.login import *


@app.route('/')
@app.route('/home')
def home():
    podcasts = youtube.get()
    if flask_login.current_user.is_anonymous:
        title = 'Youtube Podcasts'
    else:
        title = flask_login.current_user.id
    return render_template(
        'yp/index.html',
        title='Youtube Podcasts - Home Page',
        homelabel=title,
        year=datetime.now().year,
        podcasts=podcasts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    link = None
    result = None
    if request.method == 'POST' and 'link' in request.form:
        link = request.form['link']
        result = youtube.download(link)
        if result:
            return redirect("/")
        else:
            result = "Download error"
    return render_template(
        'yp/add.html',
        error=result)


@app.route('/contact')
def contact():
    return render_template(
        'yp/contact.html',
        title='Youtube Podcasts - Contact',
        year=datetime.now().year)

@app.route('/about')
def about():
    return render_template(
        'yp/about.html',
        title='Youtube Podcasts - About',
        year=datetime.now().year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_page = render_template(
        'yp/login.html',
        title='Youtube Podcasts - Login',
        year=datetime.now().year)

    if request.method == 'GET':
        return login_page

    username = request.form['username']
    record = Users.query.filter_by(username=username).first()

    if record is None:
        return login_page

    if request.form['password'] == record.password:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect('/')

    return login_page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template(
            'yp/signup.html',
            title='Youtube Podcasts - Signup',
            year=datetime.now().year)
    login = request.form['username']
    password = request.form['password']
    if login and password:
        Users.create(Users(login, password))
        user = User()
        user.id = login
        flask_login.login_user(user)
    return redirect('/')

