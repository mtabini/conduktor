from conduktor.handlers.base import BaseHandler, authenticated
from conduktor.models import URL

class URLLogHandler(BaseHandler):
    def prepare(self):
        super().prepare()
        self.set_header('Access-Control-Allow-Methods', 'GET')

    @authenticated
    def get(self, url_id):
        url = self.db.query(URL).get(url_id)

        if not url:
            self.set_status(404, 'Not Found')
            return

        try:
            offset = self.get_offset()
            limit = self.get_limit()
    
            logs = [log.json() for log in url.logs.offset(offset).limit(limit)]

            self.write_json({
                'url': url.json(),
                'logs': logs
            })
        except AssertionError as e:
            self.report_error(e)

