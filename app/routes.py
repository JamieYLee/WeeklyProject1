from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm, EditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Jamie'}
    return render_template('index.html', user2=user, title='Home Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid login credentials.')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Thanks for logging in {}!'.format(current_user.username))
        return redirect(next_page)
    return render_template('login.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=register_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile1')
def profile1():
    return render_template('profile1.html', title='Profile Settings')

@app.route('/profile2', methods=['GET', 'POST'])
def profile2():
    profile_form = EditForm()
    if profile_form.validate_on_submit():
        if profile_form.username.data:
            current_user.username = profile_form.username.data
        if profile_form.email.data:
            current_user.email = profile_form.email.data
        db.session.commit()
        flash('Congrats! You are now registered!')
        return redirect(url_for('profile1'))
    return render_template('profile2.html', form=profile_form)


@app.route('/who')
def who():
    return render_template('who.html', title='Who Are We')

@app.route('/what')
def what():
    return render_template('what.html', title='What We DO')

@app.route('/news')
def news():
    return render_template('news.html', title='News & Events')

@app.route('/where')
def where():
    return render_template('where.html', title='Where We Work')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')
