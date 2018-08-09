import alembic.config
import asyncio
import logging
import os
import tornado.ioloop
import tornado.web
import tornado.wsgi

from tornado.options import options
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

from conduktor import settings, db, routes, models


def make_app():
    return tornado.web.Application(
        routes.routes,
        debug=options.DEBUG,
    )

def make_wsgi_app():
    logging.getLogger().setLevel(logging.INFO)
    return tornado.wsgi.WSGIAdapter(make_app())
    
def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Starting server on port {}'.format(options.PORT))
    app = make_app()
    app.listen(options.PORT)
    tornado.ioloop.IOLoop.current().start() 

def migrate():
    os.chdir(os.path.join(os.path.dirname(__file__), 'alembic'))
    
    args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    
    alembic.config.main(argv=args)


asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

if __name__ == "__main__":
    main()    

