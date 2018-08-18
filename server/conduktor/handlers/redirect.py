import urllib.parse as urlparse

from sqlalchemy.orm.exc import NoResultFound
from urllib.parse import urlencode

from conduktor.handlers.base import BaseHandler
from conduktor.models import URL

import logging

class RedirectHandler(BaseHandler):
    def get(self, slug):
        try:
            url = self.db.query(URL).filter(URL.slug==slug.lower(),URL.active==True).one()
            url.record_visit(self.db)

            original_url = list(urlparse.urlparse(self.request.full_url()))
            redirect_url = list(urlparse.urlparse(url.redirect))

            query = dict(urlparse.parse_qsl(redirect_url[4]))
            query.update(dict(urlparse.parse_qsl(original_url[4])))

            redirect_url[4] = urlencode(query)

            self.redirect(urlparse.urlunparse(redirect_url))
        except NoResultFound:
            self.set_status(404, reason='Not Found')
            self.write('Not Found')
