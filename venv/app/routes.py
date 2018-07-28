from flask import render_template, request, redirect, flash
from app.forms import LoginForm, RegistrationForm, ScheduleRangeForm
from app.forms import ToSupervisorForm, ToOperatorForm
from app import app, db
from flask_login import current_user , login_user, logout_user, login_required
from app.model import User, Timeslot, ScheduleRange
from app.update_schedule import update_week, get_week, get_open, update_week_schedule
from werkzeug.urls import url_parse
from app.update_daily_schedule import convert_to_date, update_daily

import sys, json

WEEK_MAP = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
			'Friday': 4, 'Saturday': 5, 'Sunday': 6}
WEEK_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
 				'Friday', 'Saturday', 'Sunday']


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


@app.route('/schedule/<week>', methods=['GET', 'POST'])
@login_required
def schedule_page(week):
	current_weekday = WEEK_MAP[week]
	users_dic = get_week(current_weekday)
	hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
			'18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4',
			'5', '6', '7']
	orders = ['0', '1', '2', '3', '4']
	week_list = [WEEK_LIST[(current_weekday-1)%7], WEEK_LIST[current_weekday], WEEK_LIST[(current_weekday+1)%7]]
	return render_template('schedule.html',week=week_list, users=users_dic,
	 						hours=hours, orders=orders)


@app.route('/schedule_operator/<week>', methods=['GET', 'POST'])
@login_required
def schedule_page_operator(week):
	current_weekday = WEEK_MAP[week]
	users_dic = get_week(current_weekday)
	hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
			'18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4',
			'5', '6', '7']
	orders = ['0', '1', '2', '3', '4']
	week_list = [WEEK_LIST[(current_weekday-1)%7], WEEK_LIST[current_weekday], WEEK_LIST[(current_weekday+1)%7]]
	current_name = current_user.first_name + ' ' + current_user.last_name
	return render_template('schedule_operator.html',week=week_list, users=users_dic,
	 						hours=hours, orders=orders, current_name=current_name)


@app.route('/week_schedule/<week>', methods=['GET', 'POST'])
@login_required
def week_schedule(week):
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	hours = ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
			'18', '19', '20', '21', '22', '23', '0', '1', '2', '3', '4',
			'5', '6', '7']
	orders = ['0', '1', '2', '3', '4']
	current_weekday = WEEK_MAP[week]
	slots_dic = get_open(week=current_weekday)
	week_list = [WEEK_LIST[(current_weekday-1)%7], WEEK_LIST[current_weekday], WEEK_LIST[(current_weekday+1)%7]]
	return render_template('week_schedule.html', week=week_list,
	 						hours=hours, orders=orders, selectable=slots_dic)


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
	return redirect('/week_schedule/'+WEEK_LIST[week])


@app.route('/changed_schedule', methods=['GET', 'POST'])
@login_required
def changed_schedule():
	data = request.form['data']
	decode = json.loads(data)
	result = ''
	week = decode['week']
	del decode['week']
	if not current_user.privilege:
		current_name = current_user.first_name + ' ' + current_user.last_name
		for key, value in decode.items():
			if value and value != current_name:
				flash('Invalid User ' + value + ' at slot ' + key + '!')
				decode[key] = ''
	invalid_dic = update_week_schedule(decode, week=week)
	if invalid_dic:
		for key, value in invalid_dic.items():
			flash('Invalid User ' + value + ' at slot ' + key + '!')
	return "Random Stuff"#redirect('/schedule/'+WEEK_LIST[week])
	#return render_template('/changed_week.html')


@app.route('/schedule_range', methods=['GET', 'POST'])
@login_required
def changed_schedule_period():
	if not current_user.privilege:
		flash('Only Admin can view the page!')
		return redirect('/home')
	old_form = ScheduleRange.query.all()
	if old_form:
		old_form = old_form[0]
	else:
		old_form = None
	form = ScheduleRangeForm()
	if form.validate_on_submit():
		if form.start_date.data <= form.end_date.data:
			if old_form:
				update_daily(convert_to_date(old_form.start_date, 0),
				 			convert_to_date(old_form.end_date, 0),
				 			form.start_date.data, form.end_date.data)
				old_form.start_date = form.start_date.data.strftime('%m-%d-%Y')
				old_form.end_date = form.end_date.data.strftime('%m-%d-%Y')
				db.session.commit()
			else:
				date_range = ScheduleRange(start_date=form.start_date.data.strftime('%m-%d-%Y'),
											end_date=form.end_date.data.strftime('%m-%d-%Y'))
				db.session.add(date_range)
				db.session.commit()
		else:
			flash('End Date Cannot Be Before Start Date')
	return render_template('schedule_range.html', old_form=old_form, form=form)


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
