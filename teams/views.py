from django.http import HttpResponse
import logging
from teams.models import Scorecard, ScorecardEntry, Team

from django.template import RequestContext, loader

logger = logging.getLogger(__name__)

def index(request):
    logger.error("something went right!")

    roster = [{"player_name": "Drew Brees", "points" : "20.0"}]

    rogues = Team.objects.get(espn_id='6')
    scorecard = Scorecard.objects.get(team=rogues, week=1)
    scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
    print [entry.slot for entry in scorecard_entries]

    template = loader.get_template('teams/index.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
    })
    return HttpResponse(template.render(context))
