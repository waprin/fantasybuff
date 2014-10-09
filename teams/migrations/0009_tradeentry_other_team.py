# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0008_auto_20141007_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeentry',
            name='other_team',
            field=models.ForeignKey(related_name=b'other_team', default=None, to='teams.Team'),
            preserve_default=False,
        ),
    ]
