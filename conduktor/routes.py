from conduktor.handlers.redirect import RedirectHandler
from conduktor.handlers.url import URLHandler
from conduktor.handlers.logs import URLLogHandler


routes = [
    (r'^/_/api/v1/url/(?P<url_id>\d+)/logs$', URLLogHandler),
    (r'^/_/api/v1/url/(?P<url_id>\d+)$', URLHandler),
    (r'^/_/api/v1/url/?$', URLHandler),
    (r'^/(?P<slug>[a-z0-9][a-z0-9\_\-]*)$', RedirectHandler),
]  
