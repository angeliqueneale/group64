from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from .models import Event  # Import the Event model
from .forms import EventForm
from . import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/category/<category>')
def event_category(category):
    events = Event.query.filter_by(category=category).all()
    return render_template('event-category.html', category=category, events=events)

@main_bp.route('/create-event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Convert the date string to a datetime object
        event_date = datetime.strptime(form.date.data, '%Y-%m-%d')

        # Handle file upload
        image_file = form.image.data
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/img', image_filename)
            image_file.save(image_path)

        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=event_date,
            category=form.category.data,
            status='Open',
            image=image_filename
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.home', message='Event created successfully!'))
    return render_template('create-event.html', form=form)

@main_bp.route('/booking-history')
def booking_history():
    return render_template('booking-history.html')

@main_bp.route('/sports-events')
def sports_events():
    # Fetch sports events from the database if needed
    sports_events = Event.query.filter_by(category='sports').all()
    return render_template('sports-events.html', events=sports_events)

@main_bp.route('/delete-event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    category = event.category  # Get the category before deleting
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('main.event_category', category=category, message='Event deleted successfully!'))

@main_bp.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        # Use SQLAlchemy to filter events by title or description
        events = Event.query.filter(
            (Event.title.ilike(f'%{query}%')) | (Event.description.ilike(f'%{query}%'))
        ).all()
    else:
        events = []
    return render_template('search-results.html', query=query, events=events)

@main_bp.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event-details.html', event=event)
