from django.contrib.auth.models import User
from django.db import models

import logging
logger = logging.getLogger(__name__)

class EspnUser(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

class League(models.Model):
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.CharField(max_length=5)

    loaded = models.BooleanField(default=False)

    league_scrape_start_time = models.DateTimeField(null=True)
    lineups_scrape_finish_time = models.DateTimeField(null=True)
    players_scrape_finish_time = models.DateTimeField(null=True)
    league_loaded_finish_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('espn_id', 'year',)

    def __unicode__(self):
        return "ESPN %s %s" % (self.espn_id, self.year)

class Team(models.Model):
    league = models.ForeignKey(League)
    espn_user = models.ForeignKey(EspnUser, null=True)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    abbreviation = models.CharField(max_length=10, null=True)
    owner_name = models.CharField(max_length=100, null=True)
    average_delta = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    class Meta:
        unique_together = ('league', 'espn_id',)

    def __unicode__(self):
        return "%s (%s)" % (self.team_name, self.espn_id)

class TeamReportCard(models.Model):
    team = models.OneToOneField(Team)
    lineup_score = models.DecimalField(decimal_places=4, max_digits=7)

class TeamWeekScores(models.Model):
    team = models.ForeignKey(Team, null=True)
    league = models.ForeignKey(League, null=True)
    draft_score = models.DecimalField(decimal_places=4, max_digits=7)
    week = models.IntegerField()




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
    position = models.CharField(max_length=20, choices=POSITIONS, null=True)
    espn_id = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name

class Scorecard(models.Model):
    team = models.ForeignKey(Team)
    week = models.IntegerField()
    actual = models.BooleanField(default=False)
    points = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    delta = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    class Meta:
        unique_together = ('team', 'week', 'actual')

"""
class LeagueReportCard(models.Model):
    league = models.ForeignKey(League)
    average_delta = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

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
    points = models.DecimalField(decimal_places=4, max_digits=7)
    added = models.NullBooleanField()

    def __unicode__(self):
        return "player %s position %s slot %s points %f" % (self.player.name, self.player.position,  self.slot, self.points)

    def clone(self):
            new_kwargs = dict([(fld.name, getattr(self, fld.name)) for fld in self._meta.fields if fld.name != 'id']);
            return self.__class__.objects.create(**new_kwargs)


class ScoreEntry(models.Model):
    week = models.IntegerField()
    player = models.ForeignKey(Player)
    year = models.CharField(max_length=5)

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

    pat_made = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_missed = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_0 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_40 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_50 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    return_td = models.IntegerField(null=True)

    default_points = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

class ScoringSystem(models.Model):

    py25 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    int_thrown = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    td_pass = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    twopt_pass = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    run10 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    td_rush = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    twopt_rush = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    rec10 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    rec_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    twopt_rec = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    kr_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    pr_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fum_lost = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fum_rec_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fum_ret_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    pat_made = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_missed = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_0 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_40 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    fg_50 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)

    d_sack = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_int_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_fr_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_pr_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_blocked_kick = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_fr = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_kickoff_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_blocked_td = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_int = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_sf = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_pa_0 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    d_pa_1 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_pa_7 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_pa_14 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_pa_28 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_pa_35 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_pa_46 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_100 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_199 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_299 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_399 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_449 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_499 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_549 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)
    da_ya_550 = models.DecimalField(decimal_places=4, max_digits=7, default=None, null=True)


class TransLogEntry(models.Model):
    date = models.DateField()
    team = models.ForeignKey(Team)

    class Meta:
        abstract = True

class DraftClaim(TransLogEntry):
    player_added = models.ForeignKey(Player)
    round = models.IntegerField()

class TradeEntryManager(models.Manager):

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
    objects = TradeEntryManager()


class AddDrop(TransLogEntry):
    player_added = models.ForeignKey(Player, related_name='adddrop_added')
    player_dropped = models.ForeignKey(Player, related_name='addrop_dropped')
    """waiver - true if picked from the waiver, false if picked from FA"""
    waiver = models.BooleanField(default=True)


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