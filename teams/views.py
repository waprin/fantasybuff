from django.http import HttpResponse
import logging
from teams.models import League

logger = logging.getLogger(__name__)

def index(request):
    logger.error("something went right!")

    return HttpResponse("Hello world, you're at the poll index.")
