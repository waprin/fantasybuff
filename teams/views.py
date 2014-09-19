from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
import logging
from django.shortcuts import redirect
from teams.management.commands.scrape_user import defer_espn_user_scrape
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import Scorecard, ScorecardEntry, Team, League, EspnUser
import json


from django.contrib.auth.models import User

from django.template import RequestContext, loader
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import is_scraped, is_loaded, is_league_teams_scraped, is_league_loaded, \
    is_league_players_scraped
import django_rq

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login, logout

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

@login_required
def show_team(request, espn_league_id, year, espn_team_id):
    league = League.objects.get(espn_id=espn_team_id, year=year)
    team = Team.objects.get(team=espn_team_id, league=league)
    actual_weeks = list(Scorecard.objects.filter(team=team, actual=True))
    optimal_weeks = list(Scorecard.objects.filter(team=team, actual=False))
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

@login_required()
def show_league(request, espn_id, year):
    league = League.objects.get(espn_id=espn_id, year=year)
    teams = Team.objects.filter(league=league)

    template = loader.get_template('teams/league.html')

    store = SqlStore()
    teams_scraped = is_league_teams_scraped(league, store)
    players_scraped = is_league_players_scraped(league, store)
    loaded = False
    if teams_scraped and players_scraped:
        loaded = is_league_loaded(league, store)

    context = RequestContext(request, {
        'teams': teams,
        'navigation': ['Lineup Home', league.name + ' ' + str(league.year)],
        'teams_scraped': teams_scraped,
        'players_scraped': players_scraped,
        'loaded': loaded,
    })


    return HttpResponse(template.render(context))


from django.core import serializers

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

    accounts= []
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

    espn_user, created = EspnUser.objects.get_or_create(user=request.user, username=username, password=password)

    django_rq.enqueue(defer_espn_user_scrape, espn_user)
    return redirect(show_all_leagues)


