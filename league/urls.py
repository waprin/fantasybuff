from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
import settings

# Uncomment the next two lines to enable the admin: 
from django.contrib import admin
admin.autodiscover()

from django.shortcuts import redirect

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'league.views.home', name='home'),
    # url(r'^league/', include('league.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

     url(r'^signin/$', 'teams.views.signin'),
     url(r'^signin/signup/$', 'teams.views.signup'),
     url(r'^logout/$', 'teams.views.logout_user'),

     url(r'^$', 'teams.views.show_all_leagues'),
     url(r'^json/$', 'teams.views.get_all_leagues_json'),
     url(r'^espn/$', 'teams.views.espn_create'),

     url(r'^league/(\d*)/(\d\d\d\d)/$', 'teams.views.show_league'),
     url(r'^league/(\d*)/(\d\d\d\d)/(\d*)/$', 'teams.views.show_team'),
     url(r'^league/(\d*)/(\d\d\d\d)/(\d*)/(\d*)', 'teams.views.show_week'),
     url(r'', include('social_auth.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    (r'^django-rq/', include('django_rq.urls')),
)