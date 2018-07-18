from conduktor.handlers.url import URLHandler

routes = [
    (r'^/_/api/v1/url/(?P<url_id>.+)$', URLHandler)
]
