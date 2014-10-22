# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0018_auto_20141016_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='pages_scraped',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='league',
            name='total_pages',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
