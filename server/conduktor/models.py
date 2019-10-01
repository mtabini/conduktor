import datetime
import re
import validators

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates


BaseModel = declarative_base()

class URL(BaseModel):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, unique=True)
    redirect = Column(String(4096), nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, default=true(), nullable=False)

    @validates('slug')
    def validate_slug(self, key, field):
        if not isinstance(field, str):
            raise AssertionError('The `slug` field must be a string')

        if not re.match(r'^[a-z0-9][a-z0-9\-_]{2,}$', field):
            raise AssertionError('The `slug` field must be at least 3 characters long, start with a letter or noumber, and can only contain letters, numbers, underscores, and dashes.')

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

    def record_visit(self, db):
        db.execute(
            '''
                INSERT INTO 
                    url_stats (
                        url_id,
                        date_created,
                        "count"
                    )
                VALUES
                    (
                        :url_id,
                        :date_created,
                        1
                    )
                ON CONFLICT(url_id, date_created)
                DO UPDATE SET "count" = excluded."count" + 1
            ''',
            {
                'url_id': self.id,
                'date_created': datetime.date.today().replace(day=1),
            }
        )

    def json(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'redirect': self.redirect,
            'description': self.description,
            'active': self.active,
            'stats': [stat.json() for stat in self.stats[0:12]]
        }
        


class URLLog(BaseModel):
    __tablename__ = 'url_log'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    log_info = Column(String(4096), nullable=False)

    url = relationship('URL', back_populates='logs')

    def json(self):
        return {
            'date_created': self.date_created.timestamp(),
            'log_info': self.log_info,
        }


URL.logs = relationship('URLLog', order_by='desc(URLLog.date_created)', lazy='dynamic', back_populates='url')


class URLStat(BaseModel):
    __tablename__ = 'url_stats'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    count = Column(Integer, default=0, nullable=False)

    url = relationship('URL', back_populates='stats')

    def json(self):
        return {
            'date_created': self.date_created.timestamp(),
            'count': self.count,
        }


URL.stats = relationship('URLStat', order_by=URLStat.date_created, back_populates='url')
