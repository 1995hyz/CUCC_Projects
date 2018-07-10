from flask import render_template, request, redirect, flash
from app.forms import LoginForm, RegistrationForm
from app import app, db
from flask_login import current_user , login_user, logout_user, login_required
from app.model import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect('/home')
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/login')
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = '/login'
		return redirect(next_page)
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')


@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect('/home')
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
		 			first_name=form.first_name.data,
		 			last_name=form.last_name.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You have completed the registration.')
		return redirect('/login')
	return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
	#This function will return the user profile. (Being developed later)
	return render_template('profile.html', user=current_user)


@app.route('/external')
def external_links():
	'''This function will redirect to some exteranl links
	such as ccwiki and CUPS'''
	return render_template('external.html')
