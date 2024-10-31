from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum


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
    comments = db.relationship('Comment', backref='event')
    capacity = db.Column(db.Integer, nullable=False, default=100)
    category = db.Column(Enum('music', 'art', 'technology', 'sports', name='event_category'), nullable=False)
    status=db.Column(Enum('open', 'inactive', 'sold out', 'cancelled', name='event_status'), nullable=False)

	# string print method
    def __repr__(self):
        return f"<Event {self.name}, Category: {self.category}, Status: {self.status}, Owner ID: {self.owner_id}>"
    
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

