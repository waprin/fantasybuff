from django.http import HttpResponse
import logging
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import Scorecard, ScorecardEntry, Team

from django.template import RequestContext, loader

logger = logging.getLogger(__name__)

def index(request):
    rogues = Team.objects.get(espn_id='6')
    actual_weeks = list(Scorecard.objects.filter(team=rogues, actual=True))
    optimal_weeks = list(Scorecard.objects.filter(team=rogues, actual=False))
    actual_weeks.sort(key=lambda x: x.week)
    optimal_weeks.sort(key=lambda x: x.week)

    weeks = []
    for i, week in enumerate(actual_weeks):
        weeks.append({"week": week.week, "points": week.points, "optimal_points": optimal_weeks[i].points})

    print weeks
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

    actual_score = get_lineup_score(scorecard_entries)
    optimal_score = get_lineup_score(optimal_entries)

    print "actual score is " + str(actual_score)

    template = loader.get_template('teams/week.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
        'optimal_entries' : optimal_entries,
        'actual_score': actual_score,
        'optimal_score': optimal_score,
        'delta': optimal_score - actual_score
    })

    return HttpResponse(template.render(context))

def grid(request):
    template = loader.get_template('teams/grid.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
