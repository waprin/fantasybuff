# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20141007_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamweekscores',
            name='week',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
