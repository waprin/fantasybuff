from django.db.models.loading import get_models, get_app
from django.contrib import admin

for model in get_models(get_app('teams')):
    admin.site.register(model)
