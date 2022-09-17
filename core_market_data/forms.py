from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,DataRequired,Email,ValidationError
from .models import User
class RegisterForm(FlaskForm):
    username=StringField(label='Username', validators=[Length(min=2, max=30),DataRequired()])
    email_address=StringField(label='Email address', validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password', validators=[Length(min=2),DataRequired()])
    password2=PasswordField(label='Confirm password', validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='submit')

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username is already exist! Please try another username')
    def validate_email_address(self,email_address_to_check):
        user = User.query.filter_by(email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError('email address is already exist! Please try another email address')

class LoginForm(FlaskForm):
    username=StringField(label="User Name", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label='Sign In')
    
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')
    

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')