from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, DateField, TimeField, PasswordField,SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# creates the login information
class LoginForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired("Email is required")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Post')

#Create event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  description = TextAreaField('Event Description', 
            validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
  date = DateField('Event Date', format='%Y-%m-%d', validators=[InputRequired()])
  time = TimeField('Event Time', format='%H:%M', validators=[InputRequired()])
  venue = StringField('Event Venue', validators=[InputRequired()])
  category = SelectField('Category', choices=[('music', 'Music'), ('art', 'Art'), ('technology', 'Technology'), ('sports', 'Sports')], validators=[InputRequired()])
  status=SelectField('Status', choices=[('open', 'Open'), ('inactive', 'Inactive'), ('sold out', 'Sold Out'), ('cancelled', 'Cancelled')], validators=[InputRequired()])
  submit = SubmitField("Create")

class EditEventStatusForm(FlaskForm):
    status=SelectField('Status', choices=[('open', 'Open'), ('inactive', 'Inactive'), ('sold out', 'Sold Out'), ('cancelled', 'Cancelled')], validators=[InputRequired()])
    submit = SubmitField('Update ')

class BookingForm(FlaskForm):
    # You can add fields for additional booking details
    name = StringField('Your Name', validators=[InputRequired()])
    number_of_tickets = SelectField('Number of Tickets', 
                                      choices=[(i, str(i)) for i in range(1, 5)],  # Dropdown from 1 to 10
                                      validators=[InputRequired()])
    submit = SubmitField('Book Now')