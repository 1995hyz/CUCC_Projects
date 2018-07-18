from flask import render_template, request, redirect, flash
from app.forms import LoginForm, RegistrationForm
from app.forms import ToSupervisorForm, ToOperatorForm
from app import app, db
from flask_login import current_user , login_user, logout_user, login_required
from app.model import User, Timeslot
from app.update_schedule import update_week, get_week
from werkzeug.urls import url_parse

import sys, json


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
		 			last_name=form.last_name.data,
					privilege=False)
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


@app.route('/admin')
@login_required
def admin_page():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	return render_template('admin.html')


@app.route('/external')
def external_links():
	'''This function will redirect to some exteranl links
	such as ccwiki and CUPS'''
	return render_template('external.html')


@app.route('/privilege', methods=['GET', 'POST'])
@login_required
def privilege_page():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	form1 = ToSupervisorForm()
	form2 = ToOperatorForm()
	if form1.submit1.data and form1.validate_on_submit():
		user = User.query.filter_by(username=form1.username.data).first()
		if user:
			user.privilege = True
			db.session.commit()
			flash(user.username + ' has become Supervisor')
			return redirect('/privilege')
		else:
			flash('Invalid Email Account')
			return redirect('/privilege')
	if form2.submit2.data and form2.validate_on_submit():
		user = User.query.filter_by(username=form2.username.data).first()
		if user:
			user.privilege = False
			db.session.commit()
			flash(user.username + 'has become Operator')
			return redirect('/privilege')
		else:
			flash('Invalid Email Account')
			return redirect('/privilege')
	return render_template('privilege.html', user=User.query.all(),
							form2=form2, form1=form1)


@app.route('/schedule_m', methods=['GET', 'POST'])
@login_required
def schedule_page():
	users_dic = get_week(0)
	return render_template('/schedule_m.html', users=users_dic,
	 						hours=['9'], orders=['0', '1', '2', '3'])


@app.route('/week_schedule_m', methods=['GET', 'POST'])
@login_required
def week_schedule_monday():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
			'18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4',
			'5', '6', '7']
	orders = ['0', '1', '2', '3']
	slots = Timeslot.query.filter_by(week=0)
	slot_dic = {}
	for slot in slots:
		key = str(slot.time) + '/' + str(slot.index)
		slot_dic[key] = slot.open
	return render_template('/week_schedule_m.html',
	 						hours=hours, orders=orders, selectable=slot_dic)


@app.route('/week_schedule_tu', methods=['GET', 'POST'])
@login_required
def week_schedule_tuesday():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
			'18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4',
			'5', '6', '7']
	orders = ['0', '1', '2', '3']
	slots = Timeslot.query.filter_by(week=1)
	slot_dic = {}
	for slot in slots:
		key = str(slot.time) + '/' + str(slot.index)
		slot_dic[key] = slot.open
	return render_template('/week_schedule_tu.html',
	 						hours=hours, orders=orders, selectable=slot_dic)


@app.route('/changed_week', methods=['GET', 'POST'])
@login_required
def changed_week():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	data = request.form['data']
	decode = json.loads(data)
	result = ''
	week = decode['week']
	del decode['week']
	update_week(decode, week=week)
	return render_template('/changed_week.html')


@app.route('/test', methods=['POST'])
def test():
	data = request.form['data']
	decode = json.loads(data)
	result = ''
	update_week(decode)
	'''for item in data:
		# loop over every row
		result += str(item['make']) + '\n'
	return result'''
	#return render_template('/test.html')
