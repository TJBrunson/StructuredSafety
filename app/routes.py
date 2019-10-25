from flask import render_template
from app import app
from app.forms import UserLoginForm, CompanyLoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Tim'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    return render_template('login.html', title="Choose an account type")

@app.route('/user_login')
def userLogin():
    form = UserLoginForm()
    return render_template('user_login.html', title="Sign In", form=form)

@app.route('company_login')
def companyLogin():
    form = CompanyLoginForm()
    return render_template('company_login.html', title="Sign In", form=form)