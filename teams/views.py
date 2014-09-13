from django.http import HttpResponse
import logging
from teams.metrics.lineup_calculator import calculate_optimal_lineup
from teams.models import Scorecard, ScorecardEntry, Team

from django.template import RequestContext, loader

logger = logging.getLogger(__name__)

def index(request):
    rogues = Team.objects.get(espn_id='6')
    scorecard = Scorecard.objects.get(team=rogues, week=1)
    scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
    print [entry.slot for entry in scorecard_entries]

    optimal_entries = calculate_optimal_lineup(scorecard_entries)

    template = loader.get_template('teams/index.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
        'optimal_entries' : optimal_entries
    })

    return HttpResponse(template.render(context))

def show_week(request, week):
    rogues = Team.objects.get(espn_id='6')
    scorecard = Scorecard.objects.get(team=rogues, week=int(week))
    scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
    print [entry.slot for entry in scorecard_entries]

    optimal_entries = calculate_optimal_lineup(scorecard_entries)

    template = loader.get_template('teams/index.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
        'optimal_entries' : optimal_entries
    })

    return HttpResponse(template.render(context))