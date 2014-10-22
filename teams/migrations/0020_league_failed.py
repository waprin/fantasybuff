# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0019_auto_20141019_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='failed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
