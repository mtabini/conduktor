import datetime
import re
import validators

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from tornado.escape import json_encode


BaseModel = declarative_base()

class URL(BaseModel):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, unique=True)
    redirect = Column(String(4096), nullable=False)
    description = Column(String, nullable=False)

    @validates('slug')
    def validate_slug(self, key, field):
        if not isinstance(field, str):
            raise AssertionError('The `slug` field must be a string')

        if not re.match(r'^[a-z0-9][a-z0-9\-_]{3,}$', field):
            raise AssertionError('The `slug` field must be at least 4 characters long, start with a letter or noumber, and can only contain letters, numbers, underscores, and dashes.')

        return field.lower()

    @validates('redirect')
    def validate_redirect(self, key, field):
        if not isinstance(field, str):
            raise AssertionError('The `redirect` field must be a string')
            
        if not validators.url(field):
            raise AssertionError('The `redirect` field must be a valid URL.')

        return field

    @validates('description')
    def validate_description(self, key, field):
        if not isinstance(field, str):
            raise AssertionError('The `description` field must be a string')

        return field

    def to_json(self):
        return json_encode({
            'id': self.id,
            'slug': self.slug,
            'redirect': self.redirect,
            'description': self.description,
        })
        


class URLLog(BaseModel):
    __tablename__ = 'url_log'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    log_info = Column(String(4096), nullable=False)

    url = relationship('URL', back_populates='logs')


URL.logs = relationship('URLLog', order_by=URLLog.date_created, back_populates='url')


class URLStats(BaseModel):
    __tablename__ = 'url_stats'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    count = Column(Integer, default=0, nullable=False)