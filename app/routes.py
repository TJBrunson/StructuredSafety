from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Tim'}
    return render_template('index.html', title='Home', user=user)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/demo')
def demo():
    return render_template('demo.html')