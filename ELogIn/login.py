from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
@app.route('/login')
def log_in():
	return render_template('login.html')

@app.route('/userpage',methods=['POST'])
def log_in_success():
	email=request.form['email']
	password=request.form['password']
	return 'You have been successfully logged in as: '+str(email)

app.run()
