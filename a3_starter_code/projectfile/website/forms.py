from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from wtforms import DateTimeField, SelectField
from flask_wtf.file import FileField, FileAllowed

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class EventForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=500)])
    date = StringField('Date', validators=[InputRequired()])
    category = SelectField('Category', choices=[('music', 'Music'), ('art', 'Art'), ('technology', 'Technology'), ('sports', 'Sports')], validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Create Event')
