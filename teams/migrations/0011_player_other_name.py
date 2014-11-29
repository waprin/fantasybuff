# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0010_auto_20141122_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='other_name',
            field=models.CharField(default=None, max_length=100, null=True),
            preserve_default=True,
        ),
    ]
