import os

from tornado.options import define


def from_env(name, help, default=None):
    if name in os.environ:
        define(name, default=os.environ[name], help=help)
        return

    if default:
        define(name, default=default, help=help)
        return

    raise Exception('Missing required environment variable {}'.format(name))

from_env('DB_DSN', 'A valid DSN to the database')
from_env('DEBUG', 'Turn debug mode on', True)

from_env('PORT', 'The port on which the server should listen', 3000)

from_env('GOOGLE_OAUTH_CLIENT_ID', 'The Client ID used by this app to authenticate against GSuite')
from_env('AUTHORIZED_DOMAINS', 'A comma-separated list of domains whose users are allowed to use this app')