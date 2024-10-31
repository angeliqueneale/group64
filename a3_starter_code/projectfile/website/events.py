from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment
from .forms import EditEventStatusForm, EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    form = CommentForm()
    if not event:
       abort(404)
    return render_template('event/show.html', event=event, form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    db_file_path = check_upload_file(form)
    event = Event(
       name=form.name.data,
       description=form.description.data,
       image=db_file_path,
       date=form.date.data,
       time=form.time.data,
       venue=form.venue.data,
       category=form.category.data,
       status=form.status.data,
       owner_id=current_user.id
      )  
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    # redirect when form is valid
    return redirect(url_for('event.show', id=event.id))
  return render_template('events/create.html', form=form)

@eventbp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_name(event_id):
    # Fetch the event and ensure the user is the owner
    event = Event.query.get_or_404(event_id)
    if event.owner_id != current_user.id:
        flash("You don't have permission to edit this event.")
        return redirect(url_for('event.show', id=event_id))
    
    form =EditEventStatusForm(obj=event)  # Populate the form with the current name
    
    if form.validate_on_submit():
        # Update only the name field
        event.status = form.status.data
        db.session.commit()  # Save changes to the database
        
        flash("Event status updated successfully", "success")
        return redirect(url_for('event.show', id=event_id))
    
    return render_template('events/edit.html', form=form, event=event)


def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      # read the comment from the form
      comment = Comment(text=form.text.data, event=event, user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))