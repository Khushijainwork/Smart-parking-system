from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, DateField, TimeField
from wtforms.validators import InputRequired, ValidationError, Optional, EqualTo, Regexp, Length, NumberRange

from website.models import User

class SignupForm(FlaskForm):
    """ Form to register a new account """
    username_new = StringField('Username', validators=[InputRequired(), Length(min=5, max=20,
        message='Your username should be between 3 and 20 characters long')])
    password_new = PasswordField('Password',
        validators=[InputRequired(), Length(min=5, max=20, message='Invalid password. Check password requirements'),
                    EqualTo('password_confirm', message='Passwords do not match. Try again')])
    password_confirm = PasswordField('Confirm password', validators=[InputRequired()])
    email = StringField('Email address',
        validators=[Optional(),
                    Regexp(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message='Invalid email address')])
    submit = SubmitField('Sign up')

    # Check username is unique
    def validate_username_new(self, username_new):
        user = User.query.filter_by(username=username_new.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please choose another one.')


class LoginForm(FlaskForm):
    """ Form to sign in to shop """
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    """ Form to send a message """
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email address',
        validators=[InputRequired(),
                    Regexp(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message='Invalid email address')])
    subject = StringField('Subject', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit = SubmitField('Send')


class ParkingForm(FlaskForm):
    """ Form to reserve parking bay  """
    name = StringField('Name:', validators=[InputRequired()])
    phone = StringField('Phone:', validators=[InputRequired()])
    car_type = SelectField('Car type:', choices=[('micro', 'Micro car'), ('hatch', 'Hatch back'), ('family', 'Family car'), ('suv', 'SUV'), ('truck', 'Truck')], validators=[InputRequired()])
    parking_bay = SelectField('Parking bay:', choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[InputRequired()])
    date = DateField('Date:', validators=[InputRequired()])
    time = SelectField('Time:', choices=[('Current', 'Current time'), ('8', '8am'), ('9', '9am'), ('10', '10am'), ('11', '11am'), ('12', '12pm'), ('13', '1pm'), ('14', '2pm'), ('15', '3pm'), ('16', '4pm'), ('17', '5pm'), ('18', '6pm')], validators=[InputRequired()])
    # duration = IntegerRangeField('Duration:', default=15, validators=[InputRequired(), NumberRange(min=15, max=360, message='Invalid duration')])
    submit = SubmitField('Reserve Spot')