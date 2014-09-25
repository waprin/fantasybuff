# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_auto_20140923_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingsHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
        migrations.CreateModel(
            name='TranslogHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('team_id', models.CharField(max_length=20)),
                ('league_id', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
    ]
