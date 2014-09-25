# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_settingshtmlscrape_transloghtmlscrape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingshtmlscrape',
            name='league',
        ),
        migrations.AddField(
            model_name='settingshtmlscrape',
            name='league_id',
            field=models.CharField(default='fake', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settingshtmlscrape',
            name='year',
            field=models.CharField(default='1998', max_length=5),
            preserve_default=False,
        ),
    ]
