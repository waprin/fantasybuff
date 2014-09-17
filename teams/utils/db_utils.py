__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from django.db import connection

from teams.models import *

def clear_test_database(fn):
    def wrapper(self):
        logger.info("clearing: conncetion queries is %s" % str(connection.queries))
        for user in EspnUser.objects.all():
            logger.info("user is %s" % user.email)
            user.delete()
        for league in League.objects.all():
            league.delete()
        for game in Game.objects.all():
            game.delete()
        fn(self)
    return wrapper
