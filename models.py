from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime
# from app import get_show_by_venue, get_show_by_artist

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def split_show_by_time(shows):
    today = datetime.now()
    data = {
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0
    }
    for show in shows:
        if show.start_time < today:
            data['past_shows'].append(show.long_dict())
            data['past_shows_count'] = data.get('past_shows_count', 0) + 1
        else:
            data['upcoming_shows'].append(show.long_dict())
            data['upcoming_shows_count'] = data.get(
                'upcoming_shows_count', 0) + 1
    return data

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

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
    artists = db.relationship('Artist', secondary="shows")

    def __init__(self, name='', city='', state='', address='', phone='', image_link='', facebook_link='', genres='', website='', seeking_talent=False, seeking_description=''):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.genres = ','.join(genres)
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description

    def update(self, id, name, city, state, address, phone, image_link, facebook_link, genres, website, seeking_talent, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.genres = ','.join(genres)
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description

    def long_dict(self):
        data = split_show_by_time(self.shows)
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
            'seeking_description': self.seeking_description,
            "past_shows": data['past_shows'],
            "upcoming_shows": data['upcoming_shows'],
            "past_shows_count": data['past_shows_count'],
            "upcoming_shows_count": data['upcoming_shows_count']
        }

    def short_dict(self):
        data = split_show_by_time(self.shows)
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link,
            "past_shows_count": data['past_shows_count'],
            "upcoming_shows_count": data['upcoming_shows_count']
        }

    def __repr__(self):
        return f'<Venue {self.id} : {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'

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
    venues = db.relationship(Venue, secondary="shows")

    def __init__(self, name='', city='', state='', phone='', image_link='', facebook_link='', genres='', website='', seeking_venue=False, seeking_description=''):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.genres = ','.join(genres)
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description

    def update(self, id, name, city, state, phone, image_link, facebook_link, genres, website, seeking_venue, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.genres = ','.join(genres)
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description

    def long_dict(self):
        data = split_show_by_time(self.shows)
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
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            "past_shows": data['past_shows'],
            "upcoming_shows": data['upcoming_shows'],
            "past_shows_count": data['past_shows_count'],
            "upcoming_shows_count": data['upcoming_shows_count']
        }

    def short_dict(self):
        data = split_show_by_time(self.shows)
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link,
            "past_shows_count": data['past_shows_count'],
            "upcoming_shows_count": data['upcoming_shows_count']
        }

    def __repr__(self):
        return f'<Artist {self.id} : {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'))
    start_time = db.Column(db.DateTime)
    venue = db.relationship('Venue', backref=db.backref('shows'))
    artist = db.relationship('Artist', backref=db.backref('shows'))

    def long_dict(self):
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M")
        }

    def dict_for_venue(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time
        }

    def dict_for_artist(self):
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            'start_time': self.start_time
        }

    def __repr__(self):
        return f'<Show {self.artist.name} at {self.venue.name}>'
