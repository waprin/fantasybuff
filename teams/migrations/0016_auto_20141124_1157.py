# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0015_auto_20141124_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglist',
            name='id',
        ),
        migrations.AlterField(
            model_name='mailinglist',
            name='email',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
