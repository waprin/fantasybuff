# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20140921_2249'),
    ]

    operations = [
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
    ]
