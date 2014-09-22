# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20140921_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscorestats',
            name='blocked_kr',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='fr_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='int_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='interceptions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='pass_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='pass_yards',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='reception_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='reception_yards',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='receptions',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='return_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='run_attempts',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='run_td',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='playerscorestats',
            name='run_yards',
            field=models.IntegerField(null=True),
        ),
    ]
