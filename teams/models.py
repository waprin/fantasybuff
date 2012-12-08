from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

class League(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.IntegerField()

class Team(models.Model):
    league = models.ForeignKey(League)
    espn_id = models.CharField(max_length=5)
    team_name = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.team_name

class StandingsPage(models.Model):
    html = models.CharField(max_length=10000)
    league = models.ForeignKey(League)
