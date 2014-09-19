from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging
from django.shortcuts import redirect
from league import settings
from teams.management.commands.scrape_user import defer_espn_user_scrape
from teams.metrics.lineup_calculator import get_lineup_score
from teams.models import Scorecard, ScorecardEntry, Team, League, EspnUser
import json
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import is_scraped, is_loaded
import django_rq
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

logger = logging.getLogger(__name__)

def signin(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        template = loader.get_template('teams/login.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(show_all_leagues)
            # Redirect to a success page.
        else:
            logger.error("disabled account")
            # Return a 'disabled account' error message
    else:
        logger.error("invalid login")
        # Return an 'invalid login' error message.

def signup(request):
    if not settings.ALLOW_SIGNUPS:
        logger.warn("Sigunp requested but rejected.");
        return HttpResponse("Sorry! Currently not accepting new signups.")
    password = request.POST['password']
    email = request.POST['email']

    User.objects.create_user(email, email, password)
    user = authenticate(username=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(show_all_leagues)
            # Redirect to a success page.
        else:
            logger.error("disabled account")
            # Return a 'disabled account' error message
    else:
        logger.error("invalid login")
        # Return an 'invalid login' error message.

def logout_user(request):
    logout(request)
    return redirect(signin)


def make_nav_bar(league, team=None, week=None):
    bar = [{'value': 'Leagues Home', 'href': '/'}]
    bar.append({'value': league.name + ' ' + str(league.year), 'href': '/league/%s/%s/' % (league.espn_id, league.year)})
    if team:
        bar.append({'value': team.team_name + ' ' + str(league.year), 'href': '/league/%s/%s/%s/' % (league.espn_id, league.year, team.espn_id)})
    if week:
        bar.append({'value': str(week), 'href': '/league/%s/%s/%s/%d/' % (league.espn_id, league.year, team.espn_id, week)})

    return bar

@login_required
def show_team(request, espn_league_id, year, espn_team_id):
    logger.debug("entering show_team")
    league = League.objects.get(espn_id=espn_league_id, year=year)
    team = Team.objects.get(espn_id=espn_team_id, league=league)
    actual_weeks = list(Scorecard.objects.filter(team=team, actual=True))
    optimal_weeks = list(Scorecard.objects.filter(team=team, actual=False))
    actual_weeks.sort(key=lambda x: x.week)
    optimal_weeks.sort(key=lambda x: x.week)
    logger.debug("got all deltas")

    deltas = []

    weeks = []
    for i, week in enumerate(actual_weeks):
        optimal_points = optimal_weeks[i].points
        delta = optimal_points - week.points
        deltas.append(delta)
        weeks.append({"week": week.week,
                      "points": week.points,
                      "optimal_points": optimal_points,
                      "delta": delta,
        })
    average_delta = sum(deltas) / Decimal(len(deltas))
    logger.debug("got average delta %f" % average_delta)

    template = loader.get_template('teams/team.html')
    context = RequestContext(request, {
        'weeks': weeks,
        'average_delta': average_delta,
        'navigation': make_nav_bar(league, team)
    })

    return HttpResponse(template.render(context))

d = { 'QB': 1,
      'RB': 2,
       'WR': 3,
       'TE': 4,
       'FLEX': 5,
       'D/ST': 6,
       'K': 8,
       'Bench': 1000,
}

def order_entries(entries):
    def slot_key(entry):
        try:
            return d[entry.slot]
        except KeyError:
            return 500
    return sorted(entries, key=slot_key)

@login_required
def show_week(request, espn_league_id, year, espn_team_id, week):
    logger.debug("entering show_week")
    league = League.objects.get(espn_id=espn_league_id, year=year)
    team = Team.objects.get(espn_id=espn_team_id, league=league)

    scorecard = Scorecard.objects.get(team=team, week=int(week), actual=True)
    scorecard_entries = list(ScorecardEntry.objects.filter(scorecard=scorecard))

    optimal_scorecard = Scorecard.objects.get(team=team, week=int(week), actual=False)
    optimal_entries = list(ScorecardEntry.objects.filter(scorecard=optimal_scorecard))

    actual_score = get_lineup_score(scorecard_entries)
    optimal_score = get_lineup_score(optimal_entries)

    logger.debug( "scorecard_entries " + str(scorecard_entries))
    scorecard_entries = order_entries(scorecard_entries)
    logger.debug("scorecard_entries sorted" + str(scorecard_entries))
    optimal_entries = order_entries(optimal_entries)

    template = loader.get_template('teams/week.html')
    context = RequestContext(request, {
        'scorecard_entries': scorecard_entries,
        'optimal_entries' : optimal_entries,
        'actual_score': actual_score,
        'optimal_score': optimal_score,
        'delta': optimal_score - actual_score,
        'navigation': make_nav_bar(league, team, int(week))
    })

    return HttpResponse(template.render(context))


@login_required()
def show_league(request, espn_id, year):
    league = League.objects.get(espn_id=espn_id, year=year)
    if not league.loaded:
        return HttpResponse("Sorry, league isn't loaded yet!")
    teams = Team.objects.filter(league=league)
    template = loader.get_template('teams/league.html')

    context = RequestContext(request, {
        'teams': teams,
        'league': league,
        'navigation': make_nav_bar(league),
    })
    return HttpResponse(template.render(context))

@login_required()
def get_all_leagues_json(request):
    store = SqlStore()
    espn_users = EspnUser.objects.filter(user=request.user)
    scraped = False
    loaded = False
    all_accounts = []
    for espn_user in espn_users:
        scraped = is_scraped(espn_user, store)
        if scraped:
            loaded = is_loaded(espn_user, store)
        leagues = League.objects.filter(users=espn_user)
        data = serializers.serialize('json', leagues, fields=('name','espn_id', 'year', 'loaded'))
        data = json.loads(data)
        all_accounts.append(data)

    response_data = {}
    response_data['accounts'] = all_accounts
    response_data['scraped'] = scraped
    response_data['loaded'] = loaded
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def show_all_leagues(request):
    template = loader.get_template('teams/all_leagues.html')
    context = RequestContext(request, {
        'navigation': ['Leagues']
    })
    return HttpResponse(template.render(context))

@login_required
def espn_create(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return redirect(show_all_leagues)

    logger.debug("creating espn user %s %s %s" % (request.user.username, username, password))
    try:
        espn_user = EspnUser.objects.filter(user=request.user, username=username, password=password)[0]
    except IndexError:
        espn_user = EspnUser.objects.create(user=request.user, username=username, password=password)




    django_rq.enqueue(defer_espn_user_scrape, espn_user)
    return redirect(show_all_leagues)


