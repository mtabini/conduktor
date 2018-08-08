from conduktor.handlers.base import BaseHandler, authenticated
from conduktor.db import session

class HealthHandler(BaseHandler):
    def head(self):
        return self.get()
        
    def get(self):
        session.execute('SELECT 1')
        self.set_status(201)

