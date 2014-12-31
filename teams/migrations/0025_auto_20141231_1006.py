# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0024_auto_20141129_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betainvite',
            name='invite',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
