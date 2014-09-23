# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_gamehtmlscrape'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('league', 'espn_id')]),
        ),
        migrations.RemoveField(
            model_name='team',
            name='league_espn_id',
        ),
        
    ]
