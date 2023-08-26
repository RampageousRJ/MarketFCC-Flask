from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self,newuser):
        user = User.query.filter_by(username=newuser.data).first()
        if user:
            raise ValidationError('Username already exists!')
    def validate_email(self,newmail):
        mail = User.query.filter_by(email=newmail.data).first()
        if mail:
            raise ValidationError('Email already exists!')
    username=StringField(label='Enter Username: ', validators=[Length(min=3,max=20,message='Length of username should be between 3 and 20'),DataRequired()]) 
    email=StringField(label='Enter Email: ',validators=[Email(message='Invalid Email Address'),DataRequired()]) 
    password1=PasswordField(label='Enter Password: ',validators=[Length(min=8,message='Length of passowrd should be 8'),DataRequired()]) 
    password2=PasswordField(label='Confirm Password: ',validators=[EqualTo('password1',message='Passwords do not match'),DataRequired()]) 
    submit=SubmitField(label='Create Account')
    recaptcha = RecaptchaField()
    
class LoginForm(FlaskForm):
    username=StringField(label='Username: ', validators=[DataRequired()]) 
    password=PasswordField(label='Password: ',validators=[DataRequired()])
    submit=SubmitField(label='Login')
    recaptcha = RecaptchaField()