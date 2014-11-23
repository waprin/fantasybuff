import datetime
from django.contrib.auth.models import User
from django.db import models

import logging
from django.db.models import Sum, Avg, Count
from teams.scraper.utils import real_num_weeks

logger = logging.getLogger(__name__)

class EspnUser(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    loaded = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    allow_save = models.BooleanField(default=False)

class League(models.Model):
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.CharField(max_length=5)

    loaded = models.BooleanField(default=False)
    loading = models.BooleanField(default=False)

    league_scrape_start_time = models.DateTimeField(null=True)
    lineups_scrape_finish_time = models.DateTimeField(null=True)
    players_scrape_finish_time = models.DateTimeField(null=True)
    league_loaded_finish_time = models.DateTimeField(null=True)

    pages_scraped = models.IntegerField(null=True)
    total_pages = models.IntegerField(null=True)

    failed = models.BooleanField(default=False)


    class Meta:
        unique_together = ('espn_id', 'year',)

    def __unicode__(self):
        return "ESPN %s %s" % (self.espn_id, self.year)


    def get_most_waiver_points(self):
        best = ScorecardEntry.objects.filter(team__league=self, scorecard__actual=True, source='W').exclude(slot='Bench').values('team_id', 'player_id').annotate(total_points=Sum('points')).order_by('total_points').reverse()[0]
        player = Player.objects.get(id=best['player_id'])
        team = Team.objects.get(id=best['team_id'])
        return {'player': player, 'team': team, 'points': best['total_points']}


    def get_most_perfect_lineups(self):
        most_perfect = Scorecard.objects.filter(team__league=self, actual=False, delta=0).values('team', 'team__espn_id').annotate(count=Count('id')).order_by('count').reverse()[0]
        team = Team.objects.get(id=most_perfect['team'])
        return {'team': team, 'count' : most_perfect['count'] }



class Team(models.Model):
    league = models.ForeignKey(League)
    espn_user = models.ForeignKey(EspnUser, null=True, blank=True)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    abbreviation = models.CharField(max_length=10, null=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    average_delta = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    class Meta:
        unique_together = ('league', 'espn_id',)

    def __unicode__(self):
        return "%s (%s)" % (self.team_name, self.espn_id)

    def get_draft_points(self, week):
        draft_claims = DraftClaim.objects.filter(team=self)
        drafted_players = [draft.player_added for draft in draft_claims]
        scorecard_entries = ScorecardEntry.objects.filter(scorecard__week=week,
                                                          scorecard__actual=True,
                                                          player__in=drafted_players)
        if scorecard_entries.count() > 0:
            return scorecard_entries.aggregate(Sum('points'))['points__sum']
        else:
            return 0



    def __get_waiver_points(self, week, added):
        add_drop_transactions = AddDrop.objects.get_before_week(self, week).filter(added=added)
        adt_players = [adt.player for adt in add_drop_transactions]
        scorecard_entries = ScorecardEntry.objects.filter(player__in=adt_players,
                                      scorecard__week=week,
                                      scorecard__actual=True).exclude(slot='Bench')
        if scorecard_entries.count() > 0:
            return scorecard_entries.aggregate(Sum('points'))['points__sum']
        else:
            return 0

    def get_waiver_points(self, week):
        return self.__get_waiver_points(week, True) - self.__get_waiver_points(week, False)

    def get_trade_points(self, week):
        trade_transactions = TradeEntry.objects.get_before_week(self, week)
        players_added = [tt.players_added.all() for tt in trade_transactions]
        players_added = [player for sublist in players_added for player in sublist]
        scorecard_entries_added = ScorecardEntry.objects.filter(player__in=players_added,
                                                          scorecard__week=week,
                                                          scorecard__actual=True).exclude(slot='Bench')
        if scorecard_entries_added.count() > 0:
            points_for = scorecard_entries_added.aggregate(Sum('points'))['points__sum']
        else:
            points_for = 0

        players_dropped = [tt.players_removed.all() for tt in trade_transactions]
        players_dropped = [player for sublist in players_dropped for player in sublist]
        scorecard_entries_dropped = ScorecardEntry.objects.filter(player__in=players_dropped,
                                                          scorecard__week=week,
                                                          scorecard__actual=True).exclude(slot='Bench')
        if scorecard_entries_dropped.count() > 0:
            points_against = scorecard_entries_dropped.aggregate(Sum('points'))['points__sum']
        else:
            points_against = 0
        return points_for - points_against

    def get_lineup_average(self):
        return TeamWeekScores.objects.filter(team=self).aggregate(Avg('lineup_score'))['lineup_score__avg']

    def get_draft_average(self):
        return TeamWeekScores.objects.filter(team=self).aggregate(Avg('draft_score'))['draft_score__avg']

    def get_waiver_average(self):
        return TeamWeekScores.objects.filter(team=self).aggregate(Avg('waiver_score'))['waiver_score__avg']

    def get_trade_average(self):
        return TeamWeekScores.objects.filter(team=self).aggregate(Avg('trade_score'))['trade_score__avg']

    def get_source_for_player(self, player, week):
        if DraftClaim.objects.filter(player_added=player, team=self).count():
            return 'D'
        elif AddDrop.objects.filter(player=player, added=True, team=self).count() > 0:
            return 'W'
        elif TradeEntry.objects.filter(players_added=player, team=self).count() > 0:
            return 'T'
        else:
            logger.error("Can't find source for player %s, default to do " % (player.name))
            return 'D'

    def get_player_with_most_waiver_points(self):
        best = ScorecardEntry.objects.filter(team=self, scorecard__actual=True, source='W').exclude(slot='Bench').values('player_id').annotate(total_points=Sum('points')).order_by('total_points').reverse()[0]
        return (Player.objects.get(id=best['player_id']), best['total_points'])



class TeamReportCard(models.Model):
    team = models.OneToOneField(Team)
    average_lineup_score = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    average_draft_score = models.DecimalField(decimal_places=4, max_digits=10)
    average_waiver_score = models.DecimalField(decimal_places=4, max_digits=10)
    average_trade_score = models.DecimalField(decimal_places=4, max_digits=10)

    @staticmethod
    def get_max(league, field):
        return getattr(TeamReportCard.objects.filter(team__league=league).order_by(field).reverse()[0], field)

    @staticmethod
    def get_min(league, field):
        return getattr(TeamReportCard.objects.filter(team__league=league).order_by(field)[0], field)

    """
    def lineup_rank(self):
        TeamReportCard.objects.filter(team__league=self.team.league, average_lineup_score__lt=self.average_lineup_score)
    """


class TeamWeekScores(models.Model):
    team = models.ForeignKey(Team, null=True)
    league = models.ForeignKey(League, null=True)
    draft_score = models.DecimalField(decimal_places=4, max_digits=10)
    waiver_score = models.DecimalField(decimal_places=4, max_digits=10)
    trade_score = models.DecimalField(decimal_places=4, max_digits=10)
    lineup_score = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    week = models.IntegerField()

    @staticmethod
    def get_max(league, field):
        return getattr(TeamWeekScores.objects.filter(team__league=league).order_by(field).reverse()[0], field)

    @staticmethod
    def get_min(league, field):
        return getattr(TeamWeekScores.objects.filter(team__league=league).order_by(field)[0], field)

class LeagueWeekScores(models.Model):
    league = models.ForeignKey(League)
    week = models.IntegerField()
    lineup_average = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    trade_average = models.DecimalField(decimal_places=4, max_digits=10)
    draft_average = models.DecimalField(decimal_places=4, max_digits=10)
    waiver_average = models.DecimalField(decimal_places=4, max_digits=10)

class Player(models.Model):
    POSITIONS = (
        (u'QB', 'Quarterback'),
        (u'WR', 'Wide Receiver'),
        (u'RB', 'Running Back'),
        (u'TE', 'Tight End'),
        (u'D/ST', 'Defense/Special Teams'),
        (u'K', 'Kicker'),
    )
    name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100, null=True, default=None)
    position = models.CharField(max_length=20, choices=POSITIONS, null=True)
    espn_id = models.CharField(max_length=20, unique=True, null=True)

    def __unicode__(self):
        return self.name

class Scorecard(models.Model):
    team = models.ForeignKey(Team)
    week = models.IntegerField()
    actual = models.BooleanField(default=False)
    points = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    delta = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    class Meta:
        unique_together = ('team', 'week', 'actual')

"""
class LeagueReportCard(models.Model):
    league = models.ForeignKey(League)
    average_delta = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

class LeagueAverageWeek(models.Model):
"""

class Game(models.Model):
    league = models.ForeignKey(League)
    week = models.IntegerField()
    first_scorecard = models.ForeignKey(Scorecard, related_name='first_scorecard')
    second_scorecard = models.ForeignKey(Scorecard, related_name='second_scorecard')
    html = models.TextField()

    def __unicode__(self):
        return "week %d: team %s vs team %s" % (self.week, self.first_scorecard.team.team_name, self.second_scorecard.team.team_name)

class ScorecardEntry(models.Model):
    SLOT_TYPES = (
        (u'QB', 'Quarterback'),
        (u'WR', 'Wide Receiver'),
        (u'RB', 'Running Back'),
        (u'TE', 'Tight End'),
        (u'FLEX', 'Flex'),
        (u'D/ST', 'Defense/Special Teams'),
        (u'K', 'Kicker'),
        (u'B', 'Bench')
    )

    scorecard = models.ForeignKey(Scorecard)
    player = models.ForeignKey(Player)
    slot = models.CharField(max_length=20, choices=SLOT_TYPES)
    points = models.DecimalField(decimal_places=4, max_digits=10)
    added = models.NullBooleanField()
    week = models.IntegerField()

    team = models.ForeignKey(Team, null=True)
    SOURCES = (
        (u'D', 'Draft'),
        (u'T', 'Trade'),
        (u'W', 'Waiver')
    )

    source = models.CharField(max_length=5, choices=SOURCES)


    @staticmethod
    def get_trade_value(players, week):
        total = 0
        starters = []
        for player in players:
            entries = ScorecardEntry.objects.filter(player=player, scorecard__week=week)
            if len(entries) > 0:
                entry = entries[0]
                if entry.slot != 'Bench':
                        total += entries[0].points
                        starters.append(entries[0])
        return (starters, total)


    def __unicode__(self):
        return "player %s position %s slot %s points %f" % (self.player.name, self.player.position,  self.slot, self.points)

    def clone(self):
            new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id']);
            return self.__class__.objects.create(**new_kwargs)


class ScoreEntry(models.Model):
    week = models.IntegerField()
    player = models.ForeignKey(Player)
    year = models.CharField(max_length=5)
    bye = models.BooleanField(default=False)

    class Meta:
        unique_together = (('week', 'player', 'year'))


class PlayerScoreStats(models.Model):
    score_entry = models.OneToOneField(ScoreEntry, primary_key=True, related_name='player_score_stats')

    pass_yards = models.IntegerField(null=True)
    pass_td = models.IntegerField(null=True)
    interceptions = models.IntegerField(null=True)

    run_attempts = models.IntegerField(null=True)
    run_yards = models.IntegerField(null=True)
    run_td = models.IntegerField(null=True)

    receptions = models.IntegerField(null=True)
    reception_yards = models.IntegerField(null=True)
    reception_td = models.IntegerField(null=True)

    return_td = models.IntegerField(null=True)

    blocked_kr = models.IntegerField(null=True)
    int_td = models.IntegerField(null=True)
    fr_td = models.IntegerField(null=True)

    pat_made = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_missed = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_0 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_40 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_50 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    return_td = models.IntegerField(null=True)

    default_points = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

class ScoringSystem(models.Model):

    py25 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    int_thrown = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    td_pass = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    twopt_pass = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    run10 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    td_rush = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    twopt_rush = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    rec10 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    rec_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    twopt_rec = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    kr_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    pr_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fum_lost = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fum_rec_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fum_ret_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    pat_made = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_missed = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_0 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_40 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    fg_50 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)

    d_sack = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_int_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_fr_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_pr_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_blocked_kick = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_fr = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_kickoff_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_blocked_td = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_int = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_sf = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_pa_0 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    d_pa_1 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_pa_7 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_pa_14 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_pa_28 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_pa_35 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_pa_46 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_100 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_199 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_299 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_399 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_449 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_499 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_549 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)
    da_ya_550 = models.DecimalField(decimal_places=4, max_digits=10, default=None, null=True)


class TransLogEntry(models.Model):
    date = models.DateField()
    team = models.ForeignKey(Team)

    class Meta:
        abstract = True

class DraftClaim(TransLogEntry):
    player_added = models.ForeignKey(Player)
    round = models.IntegerField()

class TransLogManager(models.Manager):

    def get_before_week(self, team, week):
        start = datetime.datetime(year=int(team.league.year), month=9, day=9)
        week_delta = datetime.timedelta(days=7)
        week = week - 1
        start_days = start + (week * week_delta)
    #    logger.debug("getting all add/drop entires prior to date %s " % str(start_days))
        return self.filter(team=team, date__lte=start_days)

    def create_if_not_exists(self, date, team, other_team, players_added, players_removed):
        trade_entry = self.create(team=team, other_team=other_team, date=date)
        for player in players_added:
            trade_entry.players_added.add(player)
        for player in players_removed:
            trade_entry.players_removed.add(player)
        trade_entry.save()

class TradeEntry(TransLogEntry):
    other_team = models.ForeignKey(Team, related_name="other_team")
    players_added = models.ManyToManyField(Player, related_name='trade_added')
    players_removed = models.ManyToManyField(Player, related_name='trade_dropped')
    objects = TransLogManager()

    def get_points_for_week(self, week):
        scorecard_entries_added = ScorecardEntry.objects.filter(player__in=self.players_added.all(),
                                                          scorecard__week=week,
                                                          scorecard__actual=True).exclude(slot='Bench')
        if scorecard_entries_added.count() > 0:
            return scorecard_entries_added.aggregate(Sum('points'))['points__sum']
        else:
            return 0

    def get_points_against_week(self, week):
        scorecard_entries_dropped = ScorecardEntry.objects.filter(player__in=self.players_removed.all(),
                                                          scorecard__week=week,
                                                          scorecard__actual=True).exclude(slot='Bench')
        if scorecard_entries_dropped.count() > 0:
            return scorecard_entries_dropped.aggregate(Sum('points'))['points__sum']
        else:
            return 0

    def get_total_points_for(self):
        week = real_num_weeks()
        return reduce(lambda t, w: t + self.get_points_for_week(w), range(1, week+1), 0)

    def get_total_points_against(self):
        week = real_num_weeks()
        return reduce(lambda t, w: t + self.get_points_against_week(w), range(1, week+1), 0)

    def get_value_cumulative(self):
        return abs(self.get_total_points_for() - self.get_total_points_against())


class AddDrop(TransLogEntry):
    player = models.ForeignKey(Player)
    added = models.BooleanField(default=True)
    """waiver - true if picked from the waiver, false if picked from FA"""
    waiver = models.BooleanField(default=True)
    objects = TransLogManager()

# scraper models

class HtmlScrape(models.Model):
    html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class EntranceHtmlScrape(HtmlScrape):
    user = models.ForeignKey(EspnUser)

class MatchupsWeekHtmlScrape(HtmlScrape):
    league = models.ForeignKey(League)
    week = models.IntegerField()

class StandingsHtmlScrape(HtmlScrape):
    league = models.ForeignKey(League)

class SettingsHtmlScrape(HtmlScrape):
    league_id = models.CharField(max_length=20)
    year = models.CharField(max_length=5)

class RosterHtmlScrape(HtmlScrape):
    week = models.IntegerField()
    team_id = models.CharField(max_length=10)
    league = models.ForeignKey(League)

class PlayerHtmlScrape(HtmlScrape):
    player_id = models.CharField(max_length=20)
    league = models.ForeignKey(League)

class GameHtmlScrape(HtmlScrape):
    first_team = models.CharField(max_length=20)
    second_team = models.CharField(max_length=20)
    week = models.IntegerField()
    league = models.ForeignKey(League)

class TranslogHtmlScrape(HtmlScrape):
    team_id = models.CharField(max_length=20)
    league_id = models.CharField(max_length=20)
    year = models.CharField(max_length=5)