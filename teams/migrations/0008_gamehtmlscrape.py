# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20140922_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameHtmlScrape',
            fields=[
                ('htmlscrape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teams.HtmlScrape')),
                ('first_team', models.CharField(max_length=20)),
                ('second_team', models.CharField(max_length=20)),
                ('week', models.IntegerField()),
                ('league', models.ForeignKey(to='teams.League')),
            ],
            options={
            },
            bases=('teams.htmlscrape',),
        ),
    ]
