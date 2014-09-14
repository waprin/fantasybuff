from django.http import HttpResponse
import logging
from teams.metrics.lineup_calculator import calculate_optimal_lineup
from teams.models import Scorecard, ScorecardEntry, Team

from django.template import RequestContext, loader

logger = logging.getLogger(__name__)

def index(request):
    rogues = Team.objects.get(espn_id='6')
    weeks = [entry.week for entry in Scorecard.objects.filter(team=rogues)]
    weeks.sort()

    template = loader.get_template('teams/team.html')
    context = RequestContext(request, {
        'weeks': weeks,
    })

    return HttpResponse(template.render(context))

def show_week(request, week):
    rogues = Team.objects.get(espn_id='6')
    scorecard = Scorecard.objects.get(team=rogues, week=int(week), actual=True)
    scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
    print [entry.slot for entry in scorecard_entries]

    optimal_scorecard = Scorecard.objects.get(team=rogues, week=int(week), actual=False)
    optimal_entries = ScorecardEntry.objects.filter(scorecard=optimal_scorecard)

    #optimal_entries = calculate_optimal_lineup(scorecard_entries)

    template = loader.get_template('teams/grid.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
        'optimal_entries' : optimal_entries
    })

    return HttpResponse(template.render(context))

def grid(request):
    template = loader.get_template('teams/grid.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
