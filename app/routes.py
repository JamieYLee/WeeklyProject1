from app import app
from flask import render_template, redirect, url_for

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Jamie'}
    return render_template('index.html', user2=user, title='Home Page')

@app.route('/redirect')
def goaway():
    return redirect(url_for('index'))
