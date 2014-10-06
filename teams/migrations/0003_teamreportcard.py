# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20141003_0228'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamReportCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lineup_score', models.DecimalField(max_digits=7, decimal_places=4)),
                ('team', models.ForeignKey(to='teams.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
