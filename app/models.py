from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)

shows_table = db.Table('shows_table',
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
  db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'))
)

# class ShowsTable(Base):
#   __tablename__ = 'shows_table'

#   artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key = True)
#   venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key = True)



class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer)
  artist_name = db.Column(db.String(50))
  artist_image_link = db.Column(db.String(120))
  venue_id = db.Column(db.Integer)
  venue_name = db.Column(db.String(50))
  venue_image_link = db.Column(db.String(120))
  start_time = db.Column(db.DateTime)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

  

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
  shows = db.relationship('Show', backref='artist', lazy=True)



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
  shows = db.relationship('Show', backref='venue', lazy=True)