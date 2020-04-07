from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime)
    artist = db.relationship("Artist", back_populates="venues")
    venue = db.relationship("Venue", back_populates="artists")

    def __repr__(self):
        return f'<Show {self.venue.name} : {self.artist.name}>'


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    artists = db.relationship("Show", back_populates="venue")

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': self.genres.split(','),
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description
        }

    def __repr__(self):
        return f'<Venue {self.id} : {self.name}>'

    """
    past_shows(artist_id, artist_image_link,start_time)
    upcoming_shows(artist_id, artist_image_link,start_time)
    past_shows_count(int)
    upcoming_shows_count(int) """


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    venues = db.relationship("Show", back_populates="artist")

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_talent,
            'seeking_description': self.seeking_description
        }

    def __repr__(self):
        return f'<Artist {self.id} : {self.name}>'

    """
    past_shows(venue_id, venue_name,venue_image_link,start_time)
    upcoming_shows(venue_id, venue_name,venue_image_link,start_time)
    past_shows_count(int)
    upcoming_shows_count(int) """
