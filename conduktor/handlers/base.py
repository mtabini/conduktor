import json
import logging

from tornado.escape import json_decode, json_encode
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

    def prepare(self):
        super().prepare()
        self.json_data = None

        if self.request.body:
                self.json_data = json_decode(self.request.body)

    def check_for_body_parameters(self, names):
        for name in names:
            if name not in self.json_data:
                raise AssertionError('The required parameter {} is missing.'.format(name))

    def write_json(self, data):
        self.add_header('content-type', 'application/json')
        self.write(json_encode(data))

    def report_error(self, e, status_code=400):
        self.set_status(status_code)
        self.write_json({
            'error': str(e),
        })

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
                