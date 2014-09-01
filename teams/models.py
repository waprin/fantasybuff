from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

class League(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.IntegerField()
    entry_page_html = models.TextField(null=True, default=None)
    standings_page_html = models.TextField(null=True, default=None)
    loaded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('espn_id', 'year',)

class Team(models.Model):
    league = models.ForeignKey(League)
    league_espn_id = models.CharField(max_length=30)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('league_espn_id', 'espn_id',)

    def __unicode__(self):
        return "%s (%s, %s)" % (self.team_name, self.league_espn_id, self.espn_id)

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
    position = models.CharField(max_length=20, choices=POSITIONS)

    def __unicode__(self):
        return self.name

class Scorecard(models.Model):
    team = models.ForeignKey(Team)

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
    #slot = models.CharField(max_length=20, choices=SLOT_TYPES)
    points = models.DecimalField(decimal_places=4, max_digits=7)

class TransLogEntry(models.Model):
    date = models.DateField()
    player = models.ForeignKey(Team)

    class Meta:
        abstract = True

class DraftClaim(TransLogEntry):
    player_added = models.ForeignKey(Player)
    round = models.IntegerField()

class AddDrop(TransLogEntry):
    player_added = models.ForeignKey(Player, related_name='adddrop_added')
    player_dropped = models.ForeignKey(Player, related_name='addrop_dropped')
    """waiver - true if picked from the waiver, false if picked from FA"""
    waiver = models.BooleanField()










