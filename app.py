import os
from traceback import print_exc
from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import validators, ValidationError
from flask_wtf import Form
from form import EditForm, RegisterForm, Update
app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/qruizer/new_database.db'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(250))
    confirm_password = db.column('confirm_password' , db.String(250))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)
    #todos = db.relationship('Todo' , backref='user',lazy='dynamic')
    def __init__(self , username ,password , email):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()
    def set_password(self , password):
        self.password = generate_password_hash(password)
    def check_password(self , password):
        return check_password_hash(self.password , password)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return '<User %r>' % (self.username)

@app.route('/')
def main():
    return render_template('main.html')

@login_required
@app.route('/logged_in')
def view():
    return render_template('view.html')

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    form = RegisterForm()
    user = User(request.form['username'] , request.form['password'], request.form['email'])
    if form.password.data == form.Retype_password.data:
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))
    else:
        flash('Passwords are not same..')
        return redirect(url_for('register'))

@login_required
@app.route('/update', methods=['GET','POST'])
def update():
    form = Update()
    if request.method == 'POST':
        g.user = User.query.get(session['user_id'])
        g.user.username = request.form['username']
        g.user.email = request.form['email']
        db.session.add(g.user)
        db.session.commit()
        flash('User Details updated')
    return render_template('update.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = True
    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid' , 'error')
        return redirect(url_for('login'))

    if not registered_user.check_password(password):
        flash('Password is invalid','error')
        return redirect(url_for('login'))

    login_user(registered_user, remember = remember_me)
    flash('Logged in successfully')
    return redirect(url_for('view'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_required
@app.route('/resetpassword', methods=['GET','POST'] )
def resetpassword():
    #if 'user_id' in session:
    form = EditForm()
    if request.method == 'POST':
        g.user = User.query.get(session['user_id'])
        if form.password.data == '':
            flash('invalid password')
        elif form.password.data == form.Retype_password.data:
            g.user.set_password(form.password.data)
            db.session.add(g.user)
            db.session.commit()
            flash('User password updated')
        else:
            flash('Check you password.')
    return render_template('resetpassword.html', form=form )

@app.before_request
def before_request():
    print session
    if 'user_id' in session:
        print session['user_id']
        g.user = User.query.get(session['user_id'])
    print current_user.is_authenticated
    g.user = current_user

if __name__ == '__main__':
    app.run(debug = True)
