from conduktor.handlers.base import BaseHandler
from conduktor.models import URL

class URLLogHandler(BaseHandler):
    def get(self, url_id):
        url = self.db.query(URL).get(url_id)

        if not url:
            self.set_status(404, 'Not Found')
            return

        try:
            logs = [log.json() for log in url.logs.offset(self.get_offset()).limit(self.get_limit())]
        except AssertionError as e:
            self.report_error(e)
            return

        self.write_json(logs)

        return
