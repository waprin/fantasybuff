# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddDrop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('waiver', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DraftClaim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('round', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EspnUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField()),
                ('html', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HtmlScrape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('html', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntranceHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('user', models.ForeignKey(to='teams.EspnUser')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('espn_id', models.CharField(max_length=30)),
                ('year', models.CharField(max_length=5)),
                ('loaded', models.DateField(null=True)),
                ('users', models.ManyToManyField(to='teams.EspnUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchupsWeekHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('week', models.IntegerField()),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=20, choices=[('QB', b'Quarterback'), ('WR', b'Wide Receiver'), ('RB', b'Running Back'), ('TE', b'Tight End'), ('D/ST', b'Defense/Special Teams'), ('K', b'Kicker')])),
                ('espn_id', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('player_id', models.CharField(max_length=20)),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='RosterHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('week', models.IntegerField()),
                ('team_id', models.CharField(max_length=10)),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='Scorecard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField()),
                ('actual', models.BooleanField()),
                ('points', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScorecardEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.CharField(max_length=20, choices=[('QB', b'Quarterback'), ('WR', b'Wide Receiver'), ('RB', b'Running Back'), ('TE', b'Tight End'), ('FLEX', b'Flex'), ('D/ST', b'Defense/Special Teams'), ('K', b'Kicker'), ('B', b'Bench')])),
                ('points', models.DecimalField(max_digits=7, decimal_places=4)),
                ('player', models.ForeignKey(to='teams.Player')),
                ('scorecard', models.ForeignKey(to='teams.Scorecard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScoreEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField()),
                ('points', models.DecimalField(max_digits=7, decimal_places=4)),
                ('league', models.ForeignKey(to='teams.League')),
                ('player', models.ForeignKey(to='teams.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StandingsHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league_espn_id', models.CharField(max_length=30)),
                ('espn_id', models.CharField(max_length=5)),
                ('team_name', models.CharField(max_length=100, null=True)),
                ('owner_name', models.CharField(max_length=100, null=True)),
                ('average_delta', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('league_espn_id', 'espn_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='scoreentry',
            unique_together=set([('week', 'player', 'league')]),
        ),
        migrations.AddField(
            model_name='scorecard',
            name='team',
            field=models.ForeignKey(to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='scorecard',
            unique_together=set([('team', 'week', 'actual')]),
        ),
        migrations.AlterUniqueTogether(
            name='league',
            unique_together=set([('espn_id', 'year')]),
        ),
        migrations.AddField(
            model_name='game',
            name='first_scorecard',
            field=models.ForeignKey(related_name=b'first_scorecard', to='teams.Scorecard'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(to='teams.League'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='second_scorecard',
            field=models.ForeignKey(related_name=b'second_scorecard', to='teams.Scorecard'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='draftclaim',
            name='player',
            field=models.ForeignKey(to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='draftclaim',
            name='player_added',
            field=models.ForeignKey(to='teams.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adddrop',
            name='player',
            field=models.ForeignKey(to='teams.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adddrop',
            name='player_added',
            field=models.ForeignKey(related_name=b'adddrop_added', to='teams.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adddrop',
            name='player_dropped',
            field=models.ForeignKey(related_name=b'addrop_dropped', to='teams.Player'),
            preserve_default=True,
        ),
    ]
