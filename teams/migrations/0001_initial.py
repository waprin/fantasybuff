# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('teams_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('teams', ['User'])

        # Adding model 'League'
        db.create_table('teams_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('espn_id', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('teams', ['League'])

        # Adding M2M table for field user on 'League'
        db.create_table('teams_league_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('league', models.ForeignKey(orm['teams.league'], null=False)),
            ('user', models.ForeignKey(orm['teams.user'], null=False))
        ))
        db.create_unique('teams_league_user', ['league_id', 'user_id'])

        # Adding model 'Team'
        db.create_table('teams_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.League'])),
            ('espn_id', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('teams', ['Team'])

        # Adding model 'StandingsPage'
        db.create_table('teams_standingspage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['teams.League'])),
        ))
        db.send_create_signal('teams', ['StandingsPage'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('teams_user')

        # Deleting model 'League'
        db.delete_table('teams_league')

        # Removing M2M table for field user on 'League'
        db.delete_table('teams_league_user')

        # Deleting model 'Team'
        db.delete_table('teams_team')

        # Deleting model 'StandingsPage'
        db.delete_table('teams_standingspage')


    models = {
        'teams.league': {
            'Meta': {'object_name': 'League'},
            'espn_id': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['teams.User']", 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'teams.standingspage': {
            'Meta': {'object_name': 'StandingsPage'},
            'html': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.League']"})
        },
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'espn_id': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['teams.League']"})
        },
        'teams.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['teams']