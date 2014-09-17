from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging
from django.shortcuts import redirect
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import Scorecard, ScorecardEntry, Team, League, EspnUser

from django.contrib.auth.models import User

from django.template import RequestContext, loader
from teams.scraper.SqlStore import SqlStore
from teams.scraper.scraper import is_scraped, is_loaded, is_league_teams_scraped_, is_league_loaded, \
    is_league_players_scraped

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

@login_required()
def show_league(request, espn_id, year):
    league = League.objects.get(espn_id=espn_id, year=year)
    teams = Team.objects.filter(league=league)

    template = loader.get_template('teams/league.html')

    store = SqlStore()
    teams_scraped = is_league_teams_scraped_(league, store)
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


@login_required
def show_all_leagues(request):
    espn_users = EspnUser.objects.filter(user=request.user)
    accounts= []

    store = SqlStore()

    for espn_user in espn_users:
        loaded = False
        scraped = is_scraped(espn_user, store)
        if scraped:
            loaded = is_loaded(espn_user, store)
        leagues = League.objects.filter(users=espn_user)
        accounts.append({'is_scraped': scraped, 'is_loaded': loaded, 'leagues': leagues, 'espn_user': espn_user})

    template = loader.get_template('teams/all_leagues.html')
    context = RequestContext(request, {
        'accounts': accounts,
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

    EspnUser.objects.create(user=request.user, username=username, password=password)
    return redirect(show_all_leagues)


