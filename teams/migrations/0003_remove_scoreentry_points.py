# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20140921_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoreentry',
            name='points',
        ),
    ]
