__author__ = 'bprin'

logger = logging.getLogger(__name__)

from teams.models import *


def clearDb():
    User.objects.all().delete()
    EspnUser.objects.all().delete()
    League.objects.all().delete()
    Player.objects.all().delete()
    Team.objects.all().delete()
    DraftClaim.objects.all().delete()

