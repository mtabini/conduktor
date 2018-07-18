from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from tornado.options import options


engine = create_engine(
    options.DB_DSN,
    encoding='utf-8',
    echo=True,
    pool_recycle=600,
    pool_size=20,
    max_overflow=100
)

session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=True,
        expire_on_commit=False,
    )
)