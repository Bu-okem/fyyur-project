#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

shows_table = db.Table('shows_table',
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
  db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'))
)

class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer)
  artist_name = db.Column(db.String(50))
  artist_image_link = db.Column(db.String(120))
  venue_id = db.Column(db.Integer)
  venue_name = db.Column(db.String(50))
  start_time = db.Column(db.String(50))

class Area(db.Model):
  __tablename__ = 'areas'

  # The area table contains the list of cities and states, with the venues in those cities  
  id = db.Column(db.Integer, primary_key=True)
  state = db.Column(db.String(120))
  city = db.Column(db.String(120))
  venues = db.relationship('Venue', backref='area', lazy=True)

class Artist(db.Model):
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(120))
  performing = db.relationship('Venue', secondary=shows_table, backref='performers')

  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Venue(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(120))
  area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

db.create_all()

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  # Query the 10 latest entries in the Artist table (DESC, LIMIT) SELECT * FROM artists ORDER BY id DESC LIMIT 4;
  artists = Artist.query.order_by(desc('id')).limit(10).all()

  # Query the 10 latest entries in the Venue table (DESC, LIMIT) SELECT * FROM venues ORDER BY id DESC LIMIT 4;
  venues = Venue.query.order_by(desc('id')).limit(10).all()

  return render_template('pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------
# -- SHOW VENUES
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data=Area.query.order_by('state').all() # Query data from the Area table
  return render_template('pages/venues.html', areas=data);

# -- SEARCH VENUE
@app.route('/venues/search', methods=['POST'])
def search_venues():
  form = SearchForm()
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all() # Query returns a list

  response={
    "count": len(venues), # Get count by checking the length of the list
    "data": venues
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term, form=form)

# -- SHOW VENUE
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  data = Venue.query.filter_by(id=venue_id).first() # Query a venue from the Venue table using venue_id (SELECT * FROM venue WHERE id = venue_id) 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  error = False
  try:
    # Get input and set them into variables
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    if request.form.get('seeking_talent') == 'y': # The checkbox passes 'y' when checked and None when unchecked
      seeking_talent = True
    else:
      seeking_talent = False
    seeking_description = request.form.get('seeking_description')

    area = Area.query.filter_by(city=city).first() # Check if the area is already in the Area table

    if area is None: # If it isn't, INSERT it 
      area = Area(state=state, city=city)
      db.session.add(area)
    
    venue = Venue(name=name, address=address, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description, area=area)


    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

# -- DELETE VENUE
@app.route('/venues/<venue_id>/delete')
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    shows = Show.query.filter_by(venue_id=venue.id).all()

    db.session.delete(venue)
    for show in shows: # Delete every show the venue is associated to
      db.session.delete(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)

  return redirect(url_for('venues', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------
# -- SHOW ARTISTS
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

# -- SEARCH ARTIST
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  form = SearchForm()
  
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all() # Query returns a list

  response={
    "count": len(artists), # Get count by checking the length of the list
    "data": artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term, form=form)

# -- SHOW ARTIST
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  data = Artist.query.filter_by(id=artist_id).first() # SELECT * FROM artists WHERE id = artist_id
  # list(filter(lambda d: d['id'] == artist_id, ))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
# -- EDIT ARTIST
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.filter_by(id=artist_id).first()

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.filter_by(id=artist_id).first()

    # Update the table with whatever is passed through the form
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.address = request.form.get('address')
    artist.phone = request.form.get('phone')
    artist.image_link = request.form.get('image_link')
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website_link = request.form.get('website_link')
    if request.form.get('seeking_talent') == 'y':  # The checkbox passes 'y' when checked and None when unchecked
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False
    artist.seeking_description = request.form.get('seeking_description')
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)

  return redirect(url_for('show_artist', artist_id=artist_id))

# -- EDIT VENUE
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()

  venue = Venue.query.filter_by(id=venue_id).first()
  area = Area.query.filter_by(id=venue.area_id).first()

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue, area=area)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    areas = Area.query.order_by('id').all()

    area_city = request.form.get('city')
    area_state = request.form.get('state')

    for area in areas:
      if area.city == area_city: # If the updated city is in the table, query it and break
        area = Area.query.filter_by(city=area_city).first()
        break
      else:                     # If it isn't, INSERT it
        area = Area(city=area_city, state=area_state)
        db.session.add(area)
        db.session.commit()
        area = Area.query.filter_by(city=area_city).first()
        break
    
    # Update the table with data gotten from the form
    venue.name = request.form.get('name')
    venue.area_id = area.id
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.image_link = request.form.get('image_link')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get('facebook_link')
    venue.website_link = request.form.get('website_link')
    if request.form.get('seeking_talent') == 'y':  # The checkbox passes 'y' when checked and None when unchecked
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False
    venue.seeking_description = request.form.get('seeking_description')

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website_link = request.form.get('website_link')
    if request.form.get('seeking_venue') == 'y':  # The checkbox passes 'y' when checked and None when unchecked
      seeking_venue = True
    else:
      seeking_venue = False
    seeking_description = request.form.get('seeking_description')
    
    artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, facebook_link=facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)

    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

# -- DELETE ARTIST
@app.route('/artists/<artist_id>/delete')
def delete_artist(artist_id):
  error = False
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    shows = Show.query.filter_by(artist_id=artist.id).all()
    db.session.delete(artist)
    for show in shows: # Delete all shows associated with the artist
      db.session.delete(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)

  return redirect(url_for('artists', artist_id=artist_id))


#  Shows
#  ----------------------------------------------------------------
# DISPLAY SHOWS
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  data = Show.query.order_by('venue_id').all()
  return render_template('pages/shows.html', shows=data)

# -- CREATE SHOW
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    performer = Artist.query.filter_by(id=artist_id).first()
    show_venue = Venue.query.filter_by(id=venue_id).first()

    performer.performing.append(show_venue)
    show = Show(artist_id=performer.id, artist_name=performer.name, artist_image_link=performer.image_link, venue_id=show_venue.id, venue_name=show_venue.name, start_time=start_time)

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info()) # For reading error message
  finally:
    db.session.close()
  if error:
    abort(500)

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
