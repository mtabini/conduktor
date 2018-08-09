import os

from tornado.template import Template

from conduktor.handlers.base import BaseHandler


source = '''
window.ConduktorConfig = {
    API_URL: '{{ env['API_URL'] }}',
    AUTHORIZED_DOMAINS: '{{ env['AUTHORIZED_DOMAINS'] }}',
    GOOGLE_OAUTH_CLIENT_ID: '{{ env['GOOGLE_OAUTH_CLIENT_ID'] }}',
    APP_TITLE: '{{ env['APP_TITLE'] }}',
    BASE_URL: '{{ env['BASE_URL'] }}',
}
'''

template = Template(source)

class ClientVarsHandler(BaseHandler):
    def get(self):
        self.set_header('Content-type', 'text/javascript')
        self.write(template.generate(env=os.environ))