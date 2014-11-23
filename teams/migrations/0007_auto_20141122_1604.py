# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20141120_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoreentry',
            name='bye',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scoreentry',
            name='source',
            field=models.CharField(default=1, max_length=5, choices=[('D', b'Draft'), ('T', b'Trade'), ('W', b'Waiver')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoreentry',
            name='team',
            field=models.ForeignKey(default=1, to='teams.Team'),
            preserve_default=False,
        ),
    ]
