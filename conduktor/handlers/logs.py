from conduktor.handlers.base import BaseHandler
from conduktor.models import URL

class URLLogHandler(BaseHandler):
    def get(self, url_id):
        url = self.db.query(URL).get(url_id)

        if not url:
            self.set_status(404, 'Not Found')
            return

        logs = [log.json() for log in url.logs[self.get_offset():self.get_limit()]]

        self.write_json(logs)

        return
