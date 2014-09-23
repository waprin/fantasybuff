# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_scoringsystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerscorestats',
            name='fg_0',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerscorestats',
            name='fg_40',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerscorestats',
            name='fg_50',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerscorestats',
            name='fg_missed',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerscorestats',
            name='pat_made',
            field=models.DecimalField(default=None, null=True, max_digits=7, decimal_places=4),
            preserve_default=True,
        ),
    ]
