from conduktor.handlers.base import BaseHandler
from conduktor.models import URL


class URLHandler(BaseHandler):
    def get(self, url_id):
        url = self.db.query(URL).get(url_id)

        if not url:
            self.set_status(404, 'Not Found')
            return
        
        self.write('Found')