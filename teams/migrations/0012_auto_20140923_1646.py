# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_auto_20140923_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adddrop',
            old_name='player',
            new_name='team',
        ),
        migrations.RenameField(
            model_name='draftclaim',
            old_name='player',
            new_name='team',
        ),
    ]
