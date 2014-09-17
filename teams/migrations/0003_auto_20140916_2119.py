# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20140916_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='espnuser',
            name='user',
        ),
        migrations.AddField(
            model_name='espnuser',
            name='email',
            field=models.CharField(default='waprin@gmail.com', unique=True, max_length=200),
            preserve_default=False,
        ),
    ]
