__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from teams.models import *

def clearDb():
    for user in User.objects.all():
        user.delete()
    for user in EspnUser.objects.all():
        user.delete()
    for league in League.objects.all():
        league.delete()
    for player_stats in PlayerScoreStats.objects.all():
        player_stats.delete()

