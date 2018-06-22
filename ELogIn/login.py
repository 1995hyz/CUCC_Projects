from flask import Flask, render_template, request
from forms import LoginForm

app=Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		return redirect('/login')
	return render_template('login.html', form=form)
	
app.run()
