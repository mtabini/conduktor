from tornado import gen
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import StaticFileHandler

from conduktor.handlers import base


class StaticHandler(StaticFileHandler, GoogleOAuth2Mixin): 
    async def get(self, path, include_body=True):

        

        return await super().get(path, include_body)


    