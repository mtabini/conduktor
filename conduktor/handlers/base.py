import logging
import sys

from tornado.web import RequestHandler

from conduktor.db import session


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        self._db = None
        super().__init__(*args, **kwargs)

    @property
    def db(self):
        if not self._db:
            self._db = session()

        return self._db

    def on_finish(self):
        if self._db:
            try:
                if self.get_status() >= 200 and self.get_status() < 399:
                    self._db.commit()
                else:
                    self._db.rollback()
            except:
                logging.error('Error cleaning up database session after request end: %s', str(sys.exc_info()[0]))
                raise
            finally:
                session.remove()