from django.db import models

class User(models.Model):
    team_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class League(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200)
    espn_id = models.CharField(max_length=30)
    year = models.IntegerField()

class Team(models.Model):
    league = models.ForeignKey(League)
    espn_id = models.CharField(max_length=5)

class StandingsPage(models.Model):
    html = models.CharField(max_length=10000)
    league = models.ForeignKey(League)



