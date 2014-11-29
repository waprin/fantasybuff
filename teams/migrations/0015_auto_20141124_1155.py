# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0014_betainvite_mailinglist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglist',
            name='email',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
