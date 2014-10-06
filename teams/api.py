__author__ = 'bprin'
from tastypie.resources import ModelResource
from teams.models import Team


class TeamResource(ModelResource):
    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'