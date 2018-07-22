from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.model import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_check = PasswordField(
	'Re-enter Password', validators=[DataRequired(), EqualTo('password')])
	last_name = StringField('Last Name', validators=[DataRequired()])
	first_name = StringField('First Name', validators=[DataRequired()])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise(ValidationError('The email address has existed.'))

class ProfileForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])


class ToSupervisorForm(FlaskForm):
	username = StringField('Change To Supervisor', validators=[DataRequired(),
	 Email()])
	submit1 = SubmitField('Submit')


class ToOperatorForm(FlaskForm):
	username = StringField('Change To Operator', validators=[DataRequired(),
	 Email()])
	submit2 = SubmitField('Submit')


class ScheduleRangeForm(FlaskForm):
	start_date = DateField('Start Date',format='%m-%d-%Y',
	 						validators=[DataRequired()])
	end_date = DateField('End Date', format='%m-%d-%Y',
	 						validators=[DataRequired()])
	submit = SubmitField('Submit')
