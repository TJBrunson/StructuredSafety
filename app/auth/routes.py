from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import UserLoginForm, RegistrationForm, CompanyRegistrationForm
from app.models import User, Company, Address


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title="Sign In", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, 
            email=form.email.data, 
            first_name=form.first_name.data, 
            last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a member of Structured Safety!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/company/register', methods=['GET', 'POST'])
def companyRegistration():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        company = Company(company_name=form.company_name.data, owner_id=user.id)
        # address = Address(street_name_1=form.street_name_1.data, 
        #                   street_name_2=form.street_name_2.data, 
        #                   city=form.city.data,
        #                   state=form.state.data,
        #                   postal_code=form.postal_code.data)
        db.session.add(company)
        # db.session.add(address)
        db.session.commit()
        flash('Your company, {}, has been registered with Structured Safety!'.format(form.company_name.data))
        return redirect(url_for('main.company', company_name=form.company_name.data))
    return render_template('auth/register_company.html', title='Register a new Company', form=form)
