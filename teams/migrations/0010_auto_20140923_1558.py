# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_auto_20140923_1425'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scoreentry',
            unique_together=set([('week', 'player', 'year')]),
        ),
    ]
