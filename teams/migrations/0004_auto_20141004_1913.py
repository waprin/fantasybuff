# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_teamreportcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamreportcard',
            name='team',
            field=models.OneToOneField(to='teams.Team'),
        ),
    ]
