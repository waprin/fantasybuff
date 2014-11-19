# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_espnuser_failed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leagueweekscores',
            name='draft_average',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='leagueweekscores',
            name='lineup_average',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='leagueweekscores',
            name='trade_average',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='leagueweekscores',
            name='waiver_average',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='default_points',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='fg_0',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='fg_40',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='fg_50',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='fg_missed',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='pat_made',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='delta',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='points',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scorecardentry',
            name='points',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_blocked_kick',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_blocked_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_fr',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_fr_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_int',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_int_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_kickoff_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_pa_0',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_pa_1',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_pr_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_sack',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='d_sf',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_pa_14',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_pa_28',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_pa_35',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_pa_46',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_pa_7',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_100',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_199',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_299',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_399',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_449',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_499',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_549',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='da_ya_550',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fg_0',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fg_40',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fg_50',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fg_missed',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fum_lost',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fum_rec_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='fum_ret_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='int_thrown',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='kr_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='pat_made',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='pr_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='py25',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='rec10',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='rec_td',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='run10',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='td_pass',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='td_rush',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='twopt_pass',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='twopt_rec',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='scoringsystem',
            name='twopt_rush',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='team',
            name='average_delta',
            field=models.DecimalField(default=None, null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamreportcard',
            name='average_draft_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamreportcard',
            name='average_lineup_score',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamreportcard',
            name='average_trade_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamreportcard',
            name='average_waiver_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamweekscores',
            name='draft_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamweekscores',
            name='lineup_score',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamweekscores',
            name='trade_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='teamweekscores',
            name='waiver_score',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
    ]
