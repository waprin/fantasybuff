from decimal import Decimal
from django.http import HttpResponse
import logging
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import Scorecard, ScorecardEntry, Team, League

from django.template import RequestContext, loader

logger = logging.getLogger(__name__)

def index(request):
    rogues = Team.objects.get(espn_id='6')
    actual_weeks = list(Scorecard.objects.filter(team=rogues, actual=True))
    optimal_weeks = list(Scorecard.objects.filter(team=rogues, actual=False))
    actual_weeks.sort(key=lambda x: x.week)
    optimal_weeks.sort(key=lambda x: x.week)

    deltas = []

    weeks = []
    for i, week in enumerate(actual_weeks):
        optimal_points = optimal_weeks[i].points
        delta = optimal_points - week.points
        deltas.append(delta)
        weeks.append({"week": week.week,
                      "points": week.points,
                      "optimal_points": optimal_points,
                      "delta": delta
        })
    average_delta = sum(deltas) / Decimal(len(deltas))
    print weeks
    template = loader.get_template('teams/team.html')
    context = RequestContext(request, {
        'weeks': weeks,
        'average_delta': average_delta
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

def show_league(request, espn_id, year):
    league = League.objects.get(espn_id=espn_id, year=year)
    teams = Team.objects.filter(league=league)

    template = loader.get_template('teams/league.html')
    context = RequestContext(request, {
        'teams': teams,
        'navigation': ['Lineup Home', league.name + ' ' + str(league.year)]
    })


    return HttpResponse(template.render(context))

def show_all_leagues(request):
    leagues = League.objects.all()

    template = loader.get_template('teams/all_leagues.html')
    context = RequestContext(request, {
        'all_leagues': leagues,
        'navigation': ['Lineup Home']
    })

    return HttpResponse(template.render(context))


def grid(request):
    template = loader.get_template('teams/grid.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
