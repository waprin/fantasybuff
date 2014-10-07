import datetime
from decimal import Decimal
from teams.metrics.lineup_calculator import calculate_optimal_lineup, get_lineup_score
from teams.models import League, Team, Scorecard, ScorecardEntry, Player, TransLogEntry, DraftClaim, TeamWeekScores
from teams.scraper.html_scrapes import get_teams_from_standings, get_num_weeks_from_matchups, get_player_ids_from_lineup, \
    get_leagues_from_entrance, get_teams_from_matchups
from teams.scraper.league_loader import load_leagues_from_entrance, load_scores_from_playersheet, \
    load_teams_from_standings, load_week_from_lineup, load_scores_from_game, load_transactions_from_translog

__author__ = 'bill'

import logging
logger = logging.getLogger(__name__)


def get_real_num_weeks(num_weeks, league):
    if int(league.year) < 2014:
        return num_weeks
    now = datetime.datetime.now()

    start = datetime.datetime(year=2014, month=9, day=9)
    week = datetime.timedelta(days=7)
    start_days = [start + (weeknum * week) for weeknum in range(0, 13)]
    for i in range(0, num_weeks):
        if now < start_days[i]:
            return i
    return num_weeks

class LeagueScraper(object):

    def __init__(self, scraper, store, overwrite=False):
        self.scraper = scraper
        self.store = store
        self.overwrite = overwrite

    def create_welcome_page(self, user):
        if not self.overwrite and self.store.has_entrance(user):
            return False
        entrance_html = self.scraper.get_entrance(user)
        self.store.write_entrance(user, entrance_html)
        return True

    def create_standings_page(self, league):
        if not self.overwrite and self.store.has_standings(league):
            return False
        standings_html = self.scraper.get_standings(league)
        self.store.write_standings(league, standings_html)
        return True

    def create_settings_page(self, league):
        if not self.overwrite and self.store.has_settings(league.espn_id, league.year):
            return False
        settings_html = self.scraper.get_settings(league.espn_id, league.year)
        self.store.write_settings(league.espn_id, league.year, settings_html)
        return True

    def create_matchups_page(self, league, week):
        if not self.overwrite and self.store.has_matchups(league, week):
            return False
        matchups_html = self.scraper.get_matchups(league, week)
        self.store.write_matchups(league, week, matchups_html)
        return True

    def create_team_week_roster(self, league, team_id, week):
        if not self.overwrite and self.store.has_roster(league, team_id, week):
            return False
        roster_html = self.scraper.get_roster(league, team_id, week)
        self.store.write_roster(league, team_id, week, roster_html)
        return True

    def create_player(self, league, player_id):
        if not self.overwrite and self.store.has_player(league, player_id):
            return False
        player_html = self.scraper.get_player(player_id, league)
        self.store.write_player(league, player_id, player_html)
        return True

    def create_players_from_roster(self, league, team_id, week):
        html = self.store.get_roster(league, team_id, week)
        player_ids = get_player_ids_from_lineup(html)
        for player_id in player_ids:
            self.create_player(league, player_id)

    def create_game(self, league, team_id, week):
        logger.debug("creating game %s %s %d" % (str(league), team_id, week))
        if not self.overwrite and self.store.has_game(league, team_id, week):
            return False
        game_html = self.scraper.get_game(league, team_id, week)
        self.store.write_game(league, team_id, week, game_html)
        return True

    def create_translog(self, league, team):
        if not self.overwrite and self.store.has_translog(league.espn_id, league.year, team[0]):
            return False
        translog_html = self.scraper.get_translog(league.espn_id, league.year, team[0])
        self.store.write_translog(league.espn_id, league.year, team[0], translog_html)
        return True

    def create_weekly_matchups(self, league, week):
        logger.debug("create weekly matchups(): begin %d " % week)
        self.create_matchups_page(league, week)
        matchups_html = self.store.get_matchups(league, week)
        teams = get_teams_from_matchups(matchups_html)
        logger.debug("teams is %s" % str(teams))
        for team_id in teams:
            team_id = team_id[0]
            logger.debug("create weekly matchups(): %s %s %d" % (league, team_id, week))
            self.create_game(league, team_id, week)

    def scrape_core_and_matchups(self, league):
        league.league_scrape_start_time = datetime.datetime.now()
        league.save()
        self.create_standings_page(league)
        #self.create_settings_page(league)
        self.create_matchups_page(league, 1)
        teams = get_teams_from_standings(self.store.get_standings(league))
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        if league.year == '2013':
            for team in teams:
                for week in range(1, num_weeks + 1):
                    self.create_team_week_roster(league, team[0], week)
        elif league.year == '2014':
            logger.debug("scrape_core: 2014 logic")
            for week in range(1, num_weeks + 1):
                self.create_weekly_matchups(league, week)
        else:
            raise Exception("Unsupported year %s" % league.year)
        for team in teams:
            self.create_translog(league, team)
        league.lineups_scrape_finish_time = datetime.datetime.now()
        league.save()

    def scrape_players(self, league):
        if league.year == '2014':
            return
        teams = get_teams_from_standings(self.store.get_standings(league))
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        all_player_ids = []
        for team in teams:
            for week in range(1, num_weeks + 1):
                player_ids = get_player_ids_from_lineup(self.store.get_roster(league, team[0], week))
                all_player_ids = all_player_ids + player_ids
        all_player_ids = list(set(all_player_ids))
        for player_id in all_player_ids:
            self.create_player(league, player_id)
        league.players_scrape_finish_time = datetime.datetime.now()
        league.save()

    def scrape_league(self, league):
        self.scrape_core_and_matchups(league)
        if league.year == '2013':
            self.scrape_players(league)

    def scrape_espn_user_leagues(self, espn_user):
        logger.debug("scraping welcome page for espn user %s" % (espn_user.id))
        self.create_welcome_page(espn_user)

    def load_espn_user_leagues(self, espn_user):
        logger.debug("loading welcome page for espn user %s" % (espn_user.id))
        load_leagues_from_entrance(self.store.get_entrance(espn_user), espn_user)

    def create_leagues(self, espn_user):
        self.scrape_espn_user_leagues(espn_user)
        self.load_espn_user_leagues(espn_user)
        logger.debug("done loading leagues for espn_user %s got %d teams" % (espn_user.username, len(Team.objects.filter(espn_user=espn_user))))

    def load_league(self, league):
        league.loaded = False
        league.save()

        self.load_teams(league)

        Scorecard.objects.filter(team__league=league).delete()
        if league.year == '2013':
            self.load_players(league)
            self.load_lineups(league)
        elif league.year == '2014':
            self.load_games(league)
        else:
            raise Exception("Invalid year")

        self.load_optimal_lineups(league)
        self.load_transactions(league)
        self.load_draft_score(league)

        league.league_loaded_finish_time = datetime.datetime.now()
        league.loaded = True
        league.save()

    def reload_lineups(self, league):
        Scorecard.objects.filter(team__league=league).delete()
        self.load_lineups(league)
        self.load_optimal_lineups(league)

    def load_players(self, league):
        logger.debug("loading players for league %s" % league)
        player_htmls = self.store.get_all_player_htmls(league)
        for player_html in player_htmls:
            load_scores_from_playersheet(player_html[1], player_html[0], league.year)
        logger.debug("%d players loaded" % (len(Player.objects.all())))

    def load_teams(self, league):
        logger.debug("loading teams for league %s" % league)
        standings_html = self.store.get_standings(league)
        load_teams_from_standings(standings_html, league)

    def load_transactions(self, league):
        teams = Team.objects.filter(league=league)
        for team in teams:
            logger.debug("loading translog for team %s" % team.espn_id)
            DraftClaim.objects.filter(team=team).delete()
            transaction_html = self.store.get_translog(league.espn_id, league.year, team.espn_id)
            load_transactions_from_translog(transaction_html, team.league.year, team)

    def load_lineups(self, league):
        logger.debug("loading linups for league %s" % league)
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        teams = Team.objects.filter(league=league)
        for team in teams:
            for week in range(1, num_weeks+1):
                lineup_html = self.store.get_roster(league, team.espn_id, week)
                load_week_from_lineup(lineup_html, week, team)

    def load_games(self, league):
        Scorecard.objects.filter(team__league__id=league.id).delete()
        if league.year != '2014':
            return False
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        for week in range(1, num_weeks+1):
            htmls = self.store.get_all_games(league, week)
            for html in htmls:
                load_scores_from_game(league, week, html)

    def load_optimal_lineups(self, league):
        logger.debug("loading optimal lineups for league %s" % league)
        teams = Team.objects.filter(league=league)
        for team in teams:
            weeks = [entry.week for entry in Scorecard.objects.filter(team=team)]
            for week in weeks:
                scorecard = Scorecard.objects.get(team=team, week=week, actual=True)
                scorecard_entries = ScorecardEntry.objects.filter(scorecard=scorecard)
                logger.debug("calculating optimal lineup for team %s week %d" % (team.espn_id, week))
                optimal_entries = calculate_optimal_lineup(scorecard_entries)
                total_points = get_lineup_score(optimal_entries)
                optimal_scorecard = Scorecard.objects.create(team=team, week=week, actual=False, points=total_points)
                for entry in optimal_entries:
                    logger.debug("adding optimal scorecard entry")
                    entry.scorecard = optimal_scorecard
                    entry.save()

        for team in teams:
            logger.debug("calculating deltas for team %s" % team.team_name)
            actual_weeks = list(Scorecard.objects.filter(team=team, actual=True))
            if not actual_weeks:
                continue
            optimal_weeks = list(Scorecard.objects.filter(team=team, actual=False))
            actual_weeks.sort(key=lambda x: x.week)
            optimal_weeks.sort(key=lambda x: x.week)

            deltas = []
            for i, week in enumerate(actual_weeks):
                optimal_points = optimal_weeks[i].points
                delta = optimal_points - week.points
                optimal_weeks[i].delta = delta
                optimal_weeks[i].save()
                logger.debug("saving deltas for team %s %f" % (team.team_name, optimal_weeks[i].delta))
                deltas.append(delta)
            average_delta = sum(deltas) / Decimal(len(deltas))
            team.average_delta = average_delta
            team.save()

    def load_draft_score(self, league):
        TeamWeekScores.objects.filter(team__league=league).delete()

        teams = Team.objects.filter(league=league)
        num_weeks = get_num_weeks_from_matchups(self.store.get_matchups(league, 1))
        num_weeks = get_real_num_weeks(num_weeks, league)
        for team in teams:
            #weeks = get_real_num_weeks()
            drafts = DraftClaim.objects.filter(team=team)
            drafted_players = [draft.player_added for draft in drafts]
            for week in range(1, num_weeks+1):
                total_points = 0
                for player in drafted_players:
                    try:
                        scorecard_entry = ScorecardEntry.objects.filter(player=player, scorecard__week=week)[0]
                    except IndexError:
                        logger.debug("load_draft_scores(): Can not find scorecard entry for player %s week %d" % (player.name, week))
                        continue
                    total_points += scorecard_entry.points
                    if scorecard_entry.slot != 'Bench':
                        total_points += scorecard_entry.points
                    logger.debug("load_draft_scores(): for team %s week %d player %s points %d" %( team.team_name, week, player.name, total_points))
                TeamWeekScores.objects.create(team=team, draft_score=total_points, week=week)


















