from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Open")
    owner = db.relationship('User', backref=db.backref('events', lazy=True))
    price=db.Column(db.Integer, nullable=False)
    comments = db.relationship('Comment', backref='event')
    capacity = db.Column(db.Integer, nullable=False, default=100)
    category = db.Column(Enum('music', 'art', 'technology', 'sports', name='event_category'), nullable=False)
    status=db.Column(Enum('open', 'inactive', 'sold out', 'cancelled', name='event_status'), nullable=False)

	# string print method
    def __repr__(self):
        return f"<Event {self.name}, Category: {self.category}, Status: {self.status}, Owner ID: {self.owner_id}>"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    comments = db.relationship('Comment', backref='user')


    # Method to set password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Representation method for debugging
    def __repr__(self):
        return f'<User {self.username}>'
       
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"
    

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    number_of_tickets = db.Column(db.Integer, nullable=False) #quanity
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date of booking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when the booking was created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp of the last update
    user = db.relationship('User', backref='bookings')
    event = db.relationship('Event', backref='bookings')
    name = db.Column(db.String(100))
    def __repr__(self):
        return f'<Booking {self.id} - User: {self.user_id}, Event: {self.event_id}, Tickets: {self.number_of_tickets}>'
