import os

from tornado.web import RedirectHandler as TornadoRedirectHandler

from conduktor.handlers.redirect import RedirectHandler
from conduktor.handlers.url import URLHandler
from conduktor.handlers.logs import URLLogHandler
from conduktor.handlers.static import StaticHandler


routes = [
    (r'^/_(/?)$', TornadoRedirectHandler, {'url' : '/_/index.html'}),
    (r'^/_/api/v1/url/(?P<url_id>\d+)/logs$', URLLogHandler),
    (r'^/_/api/v1/url/(?P<url_id>\d+)$', URLHandler),
    (r'^/_/api/v1/url/?$', URLHandler),
    (r'^/(?P<slug>[a-z0-9][a-z0-9\_\-]*)$', RedirectHandler),
    (r'^/_/(.*)$', StaticHandler, {'path' : os.path.join(os.path.dirname(__file__), 'static')}),
]  
