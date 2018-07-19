from conduktor.handlers.redirect import RedirectHandler
from conduktor.handlers.url import URLHandler


routes = [
    (r'^/_/api/v1/url/?$', URLHandler),
    (r'^/_/api/v1/url/?$', URLHandler),
    (r'^/_/api/v1/url/(?P<url_id>\d+)$', URLHandler),
    (r'^/(?P<slug>[a-z0-9][a-z0-9\_\-]*)$', RedirectHandler),
]  
