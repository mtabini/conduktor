from sqlalchemy.orm.exc import NoResultFound

from conduktor.handlers.base import BaseHandler
from conduktor.models import URL


class RedirectHandler(BaseHandler):
    def get(self, slug):
        try:
            url = self.db.query(URL).filter(URL.slug==slug.lower(),URL.active==True).one()
            url.record_visit(self.db)

            self.redirect(url.redirect)
        except NoResultFound:
            self.set_status(404, reason='Not Found')
            self.write('Not Found')
