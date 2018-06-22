import flask from Flask

@app.route('/index')
def hello_world():
	return 'Hello World!'
