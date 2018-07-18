import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


BaseModel = declarative_base()

class URL(BaseModel):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False)
    redirect = Column(String(4096), nullable=False)
    description = Column(String, nullable=False)


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