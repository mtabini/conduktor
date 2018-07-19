import alembic.config
import logging
import tornado.ioloop
import tornado.web

from tornado.options import options

from conduktor import settings, db, routes, models


def make_app():
    return tornado.web.Application(
        routes.routes,
        debug=options.DEBUG,
    )

def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Starting server on port {}'.format(options.PORT))
    app = make_app()
    app.listen(options.PORT)
    tornado.ioloop.IOLoop.current().start() 

def migrate():
    args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    
    alembic.config.main(argv=args)


if __name__ == "__main__":
    main()    