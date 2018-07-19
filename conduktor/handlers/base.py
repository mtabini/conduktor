import functools
import json
import logging
import re
import sys

from tornado.auth import GoogleOAuth2Mixin
from tornado.escape import json_decode, json_encode
from tornado.web import RequestHandler, HTTPError

from conduktor.db import session


class BaseHandler(RequestHandler, GoogleOAuth2Mixin):
    def __init__(self, *args, **kwargs):
        self._db = None
        super().__init__(*args, **kwargs)

    @property
    def db(self):
        if not self._db:
            self._db = session()

        return self._db

    def options(self, *args, **kwargs):
        self.set_status(204)

    def prepare(self):
        super().prepare()

        self.json_data = None

        if self.request.body:
                self.json_data = json_decode(self.request.body)

        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Authorization,Content-Type')

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
                
    def get_offset(self):
        try:
            offset = int(self.get_query_argument('offset', 0))

            if offset < 0:
                raise AssertionError('The `limit` parameter must be a positive number less than 100')

            return offset
        except:
            raise AssertionError('The `offset` parameter must be a positive number')

    def get_limit(self):
        try:
            limit = int(self.get_query_argument('limit', 100))

            if limit < 0 or limit > 100:
                raise AssertionError('The `limit` parameter must be a positive number less than 100')

            return limit
        except:
            raise AssertionError('The `limit` parameter must be a positive number less than 100')


def authenticated(handler):
    @functools.wraps(handler)
    def auth_handler(self, *args, **kwargs):
        auth_header = self.request.headers.get('authorization', '').lower().split(' ')

        logging.info(auth_header)

        if len(auth_header) != 2 or auth_header[0] != 'token':
            raise HTTPError(403)

        return handler(self, *args, **kwargs)

    return auth_handler