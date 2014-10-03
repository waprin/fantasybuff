# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddDrop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('waiver', models.BooleanField(default=True)),
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
                ('username', models.CharField(unique=True, max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
            name='GameHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('first_team', models.CharField(max_length=20)),
                ('second_team', models.CharField(max_length=20)),
                ('week', models.IntegerField()),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
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
                ('loaded', models.BooleanField(default=False)),
                ('league_scrape_start_time', models.DateTimeField(null=True)),
                ('lineups_scrape_finish_time', models.DateTimeField(null=True)),
                ('players_scrape_finish_time', models.DateTimeField(null=True)),
                ('league_loaded_finish_time', models.DateTimeField(null=True)),
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
                ('espn_id', models.CharField(unique=True, max_length=20)),
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
                ('actual', models.BooleanField(default=False)),
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
                ('added', models.NullBooleanField()),
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
                ('year', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerScoreStats',
            fields=[
                ('score_entry', models.OneToOneField(related_name=b'player_score_stats', primary_key=True, serialize=False, to='teams.ScoreEntry')),
                ('pass_yards', models.IntegerField(null=True)),
                ('pass_td', models.IntegerField(null=True)),
                ('interceptions', models.IntegerField(null=True)),
                ('run_attempts', models.IntegerField(null=True)),
                ('run_yards', models.IntegerField(null=True)),
                ('run_td', models.IntegerField(null=True)),
                ('receptions', models.IntegerField(null=True)),
                ('reception_yards', models.IntegerField(null=True)),
                ('reception_td', models.IntegerField(null=True)),
                ('blocked_kr', models.IntegerField(null=True)),
                ('int_td', models.IntegerField(null=True)),
                ('fr_td', models.IntegerField(null=True)),
                ('pat_made', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_missed', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_0', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_40', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_50', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('return_td', models.IntegerField(null=True)),
                ('default_points', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScoringSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('py25', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('int_thrown', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('td_pass', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('twopt_pass', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('run10', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('td_rush', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('twopt_rush', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('rec10', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('rec_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('twopt_rec', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('kr_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('pr_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fum_lost', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fum_rec_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fum_ret_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('pat_made', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_missed', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_0', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_40', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('fg_50', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_sack', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_int_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_fr_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_pr_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_blocked_kick', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_fr', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_kickoff_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_blocked_td', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_int', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_sf', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_pa_0', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('d_pa_1', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_pa_7', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_pa_14', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_pa_28', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_pa_35', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_pa_46', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_100', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_199', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_299', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_399', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_449', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_499', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_549', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('da_ya_550', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SettingsHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('league_id', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
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
                ('espn_id', models.CharField(max_length=5)),
                ('team_name', models.CharField(max_length=100, null=True)),
                ('owner_name', models.CharField(max_length=100, null=True)),
                ('average_delta', models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4)),
                ('espn_user', models.ForeignKey(to='teams.EspnUser')),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TranslogHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('team_id', models.CharField(max_length=20)),
                ('league_id', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('league', 'espn_id')]),
        ),
        migrations.AddField(
            model_name='scoreentry',
            name='player',
            field=models.ForeignKey(to='teams.Player'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='scoreentry',
            unique_together=set([('week', 'player', 'year')]),
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
            model_name='gamehtmlscrape',
            name='league',
            field=models.ForeignKey(to='teams.League'),
            preserve_default=True,
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
            name='player_added',
            field=models.ForeignKey(to='teams.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='draftclaim',
            name='team',
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
        migrations.AddField(
            model_name='adddrop',
            name='team',
            field=models.ForeignKey(to='teams.Team'),
            preserve_default=True,
        ),
    ]
