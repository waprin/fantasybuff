# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20141122_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoreentry',
            name='team',
            field=models.ForeignKey(to='teams.Team', null=True),
        ),
    ]
