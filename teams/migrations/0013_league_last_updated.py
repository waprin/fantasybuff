# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_scorecardentry_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='last_updated',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
