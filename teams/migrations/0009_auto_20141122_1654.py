# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0008_auto_20141122_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoreentry',
            name='source',
        ),
        migrations.RemoveField(
            model_name='scoreentry',
            name='team',
        ),
        migrations.AddField(
            model_name='scorecardentry',
            name='source',
            field=models.CharField(default='D', max_length=5,
                                   choices=[('D', b'Draft'), ('T', b'Trade'), ('W', b'Waiver')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scorecardentry',
            name='team',
            field=models.ForeignKey(to='teams.Team', null=True),
            preserve_default=True,
        ),
    ]
