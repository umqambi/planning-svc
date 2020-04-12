from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EventAddForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    body = TextField('Описание', validators=[DataRequired()])
    start = DateTimeField('Время начала(HH:MM DD-MM-YYYY)', format='%H:%M %d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Время окончания(HH:MM DD-MM-YYYY)', format='%H:%M %d-%m-%Y', validators=[DataRequired()])
    submit = SubmitField('Создать')

class EventEditForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    body = TextField('Описание', validators=[DataRequired()])
    start = DateTimeField('Время начала(HH:MM DD-MM-YYYY)', format='%H:%M %d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Время окончания(HH:MM DD-MM-YYYY)', format='%H:%M %d-%m-%Y', validators=[DataRequired()])
    submit = SubmitField('Обновить')