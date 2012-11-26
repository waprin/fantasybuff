from django.core.management.base import BaseCommand, CommandError
from teams.models import User, League
from scrape import EspnBrowser

def init_user():
    try:
        user = User.objects.get(team_name='gothamcityrogues')
    except User.DoesNotExist:
        user = User(team_name='gothamcityrogues', password='sincere1')
        user.save()
    return user


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = init_user()
    
        browser = EspnBrower()
        browser.login(user.team_name, user.password)
        html = browser.scrape_entrance()

        m = re.search(r"leagueId=(\d*)&teamId=(\d*)&seasonId=(\d*)", html)
        league_id= m.group(1)
        team_id = m.group(2)
        season_id = m.group(3)
       
        try:
            league = League.objects.get(espn_id=league_id)
        except League.DoesNotExist:
            league = League(
            league.users.add(user)
            


       # standings = browser.scrape_standings()
        

