from sqlalchemy.exc import IntegrityError

from conduktor.handlers.base import BaseHandler
from conduktor.models import URL, URLLog


class URLHandler(BaseHandler):
    def get(self, url_id=None):
        if url_id:
            url = self.db.query(URL).get(url_id)

            if not url:
                self.set_status(404, 'Not Found')
                return
        
            self.write_json(url.json())
            return

        search_query = '%{}%'.format(self.get_query_argument('search'))

        results = [url.json() for url in self.db.query(URL).filter(URL.slug.ilike(search_query))]

        self.write_json(results)

    def post(self):
        try:
            self.check_for_body_parameters(['slug', 'redirect', 'description'])

            url = URL(
                slug=self.json_data['slug'],
                redirect=self.json_data['redirect'],
                description=self.json_data['description'],
            )

            url.logs.append(
                URLLog(
                    log_info=('Created by system.')
                )
            )

            self.db.add(url)
            self.db.commit()

            self.redirect('/_/api/v1/url/{}'.format(url.id))
        except AssertionError as e:
            self.report_error(e)
        except IntegrityError as e:
            self.report_error('Duplicate slug')