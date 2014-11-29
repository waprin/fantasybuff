# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0022_auto_20141128_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
