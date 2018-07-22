from sqlalchemy.exc import IntegrityError

from conduktor.handlers.base import BaseHandler, authenticated
from conduktor.models import URL, URLLog


class URLHandler(BaseHandler):
    def prepare(self):
        super().prepare()
        self.set_header('Access-Control-Allow-Methods', 'GET,POST,PUT,OPTIONS')

    @authenticated
    def get(self, url_id=None):
        if url_id:
            url = self.db.query(URL).get(url_id)

            if not url:
                self.set_status(404, 'Not Found')
                return
        
            self.write_json(url.json())
            return

        search_query = '%{}%'.format(self.get_query_argument('search', ''))

        offset = self.get_offset()
        limit = self.get_limit()

        results = self.db.query(URL).filter(URL.slug.ilike(search_query)).offset(offset).limit(limit)

        self.write_json([url.json() for url in results])

    @authenticated
    def put(self, url_id):
        url = self.db.query(URL).get(url_id)

        if not url:
            self.set_status(404, 'Not Found')
            return

        if 'slug' in self.json_data:
            slug = self.json_data['slug']

            if slug != url.slug:
                url.logs.append(URLLog(log_info='{} has changed the slug to `{}`'.format(self.user_name, slug)))
                url.slug = slug

        if 'redirect' in self.json_data:
            redirect = self.json_data['redirect']

            if redirect != url.redirect:
                url.logs.append(URLLog(log_info='{} has changed the redirect to `{}`'.format(self.user_name, redirect)))
                url.redirect = redirect

        if 'description' in self.json_data:
            description = self.json_data['description']

            if description != url.description:
                url.logs.append(URLLog(log_info='{} has changed the description to `{}`'.format(self.user_name, description)))
                url.description = description

        if 'active' in self.json_data:
            active = self.json_data['active']

            if active != url.active:
                if active:
                    url.logs.append(URLLog(log_info='{} has reactivated the URL forward'.format(self.user_name)))
                else:
                    url.logs.append(URLLog(log_info='{} has deactivated the URL forward'.format(self.user_name)))

                url.active = active

        try:
            self.db.commit()
            self.set_status(201)
        except IntegrityError as e:
            self.report_error('This slug already exists. Please change to a different one and try again. To edit the redirect with this slug, search for it from the main screen.')

    @authenticated
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
                    log_info='Created by system.'
                )
            )

            self.db.add(url)
            self.db.commit()

            self.redirect('/_/api/v1/url/{}'.format(url.id))
        except AssertionError as e:
            self.report_error(e)
        except IntegrityError as e:
            self.report_error('This slug already exists. Please change to a different one and try again. To edit the redirect with this slug, search for it from the main screen.')