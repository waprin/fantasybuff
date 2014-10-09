# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_teamweekscores_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('players_added', models.ManyToManyField(related_name=b'trade_added', to='teams.Player')),
                ('players_removed', models.ManyToManyField(related_name=b'trade_dropped', to='teams.Player')),
                ('team', models.ForeignKey(to='teams.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='team',
            name='abbreviation',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
    ]
